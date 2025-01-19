import pandas as pd
import numpy as np


class Topsis:
    def __init__(self, df: pd.DataFrame, weights: list, impacts: list, distance_metric: str = 'euclidean', missing_data_strategy: str = 'mean'):
        self.df = self.fill_missing_data(df, strategy=missing_data_strategy)
        self.weights = np.array(weights)
        self.impacts = impacts
        self.distance_metric = distance_metric

    def fill_missing_data(self, df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
        if strategy == 'mean':
            return df.fillna(df.mean())
        elif strategy == 'median':
            return df.fillna(df.median())
        elif strategy == 'none':
            return df
        else:
            raise ValueError(f"Invalid missing_data_strategy: '{strategy}'. Use 'mean', 'median', or 'none'.")

    def calculate(self) -> pd.DataFrame:
        numeric_cols = self.df.select_dtypes(include=['number'])
        norm_df = numeric_cols.apply(lambda x: x / np.sqrt((x ** 2).sum()), axis=0)
        norm_df = norm_df * self.weights

        # Determine ideal and negative ideal solutions
        ideal_solution = norm_df.max().values
        negative_ideal_solution = norm_df.min().values

        for i, impact in enumerate(self.impacts):
            if impact == '-':
                ideal_solution[i], negative_ideal_solution[i] = negative_ideal_solution[i], ideal_solution[i]

        # Function to calculate distance
        def calculate_distance(df: pd.DataFrame, solution: np.ndarray, metric: str) -> np.ndarray:
            if metric == 'euclidean':
                return np.sqrt(((df - solution) ** 2).sum(axis=1))
            elif metric == 'manhattan':
                return np.abs(df - solution).sum(axis=1)
            else:
                raise ValueError(f"Unsupported distance metric: '{metric}'. Use 'euclidean' or 'manhattan'.")

        distance_ideal = calculate_distance(norm_df, ideal_solution, self.distance_metric)
        distance_negative_ideal = calculate_distance(norm_df, negative_ideal_solution, self.distance_metric)

        # Calculate TOPSIS scores
        scores = distance_negative_ideal / (distance_ideal + distance_negative_ideal)

        result_df = pd.DataFrame({
            'Alternative': self.df.index,
            **numeric_cols.to_dict(orient='list'),
            'Topsis Score': scores
        })

        # Rank alternatives
        result_df['Rank'] = result_df['Topsis Score'].rank(ascending=False, method='dense')
        result_df = result_df.sort_values(by='Rank', ascending=True)
        return result_df[['Alternative', 'Topsis Score', 'Rank']]
