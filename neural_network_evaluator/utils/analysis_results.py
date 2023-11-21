"""  
CMSC Team 5
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
Written by Jack Boswell
"""

class AnalysisResults:
    """Analysis Results class that records results of CNN analysis

    This class accepts returned dictionary classes from the torch models containing the output
    of their analysis.

    Attributes:
        _results: Dictionary of all CNN model results
    """

    def __init__(self) -> None:
        """Initializes AnalysisResults class"""
        self._results = {}

    def __repr__(self) -> str:
        """Instance repr"""
        return repr(self._results)

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
    
    def get_top_result(self) -> str:
        """Returns highest confidence output of all CNN models.  Still requires implementation

        Returns:
            String of top result
        """
        #TODO: Build this function after building CNN model output
        raise NotImplementedError