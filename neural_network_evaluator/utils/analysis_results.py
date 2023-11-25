"""  
CMSC Team 5
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
Written by Jack Boswell
"""
from collections import defaultdict
from operator import itemgetter
from typing import Tuple
class AnalysisResults:
    """Analysis Results class that records results of CNN analysis

    This class accepts returned dictionary classes from the torch models containing the output
    of their analysis.

    Attributes:
        _results: Dictionary of all CNN model results
        averaged_results: Dictionary of averaged probability results with their category
    """

    def __init__(self) -> None:
        """Initializes AnalysisResults class"""
        self._results = {}
        self.averaged_results = None

    def __repr__(self) -> str:
        """Instance repr"""
        return repr(self._results)

    def validate_state(self) -> None:
        """Verifies that results exist prior to calculations

        Raises:
          RuntimeError: No results are loaded
        """
        if len(self._results) == 0:
            raise RuntimeError(f'AnalysisResults has no results loaded.  Run AnalysisResults.add_results')

    def add_result(self, result: dict) -> None:
        """Adds CNN output result to results dictionary

        Args:
          result: CNN output result as a dictionary
        """
        self._results.update(result)

    def get_results(self) -> dict:
        """Getter for all CNN output results

        Returns:
            Dictionary of results
        """
        return self._results
    
    def get_top_result(self) -> Tuple[str, float]:
        """Returns highest confidence output of all CNN models.

        Returns:
            Tuple of top result
        """

        # Raise RuntimeError if no results are loaded
        self.validate_state()

        # Iterate through each model's results to add top result to tuple and then call max to
        # get highest probability category and score
        return max((result for model in self._results for result in [self._results[model]["top_result"]]), key=itemgetter(1))

    
    def average_results(self) -> None:
        """Calculates average of categories and their probabiltiies"""

        # Raise RuntimeError if no results are loaded
        self.validate_state()

        # Use defaultdict to accumulate probabilities for each category
        category_probabilities = defaultdict(list)

        # Iterate through each model's results and accumulate probabilities for each category
        for model, results in self._results.items():
            for category, probability in results['results']:
                category_probabilities[category].append(probability)

        # Calculate the average probability for each category
        # Applied rounding to deal with floating point arithmetic limitations
        self.averaged_results = {
           category: round(sum(probabilities) / len(probabilities), 2)
            for category, probabilities in category_probabilities.items()
        }

    def get_highest_averaged_result(self) -> Tuple[str, float]:
        """Returns highest confidence output of all CNN models.

        Returns:
            Tuple of top result
        """

        # Raise RuntimeError if no results are loaded
        self.validate_state()

        # Calculate averages
        self.average_results()

        # Get category with the highest averaged probability
        highest_average_category = max(self.averaged_results, key=self.averaged_results.get)

        # Return tuple of highest averaged category and probability
        return (highest_average_category, self.averaged_results[highest_average_category])
