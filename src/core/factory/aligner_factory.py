from src.core import AlignerInterface
from src.core.types import AlignerType
from src.core.aligner import FuzzyAligner, FuzzyWuzzyAligner


class AlignerFactory:
    """
    Factory class to create transcription instances based on the model name.
    """

    @staticmethod
    def get_aligner(aligner_type: str, **kwargs) -> AlignerInterface:
        """
        Get the appropriate aligner instance based on the aligner_type.
        Args:
            - aligner_type: Type of the aligner (e.g., "fuzzy_aligner").
            - **kwargs: Additional arguments for the aligner.
        Returns:
            - An instance of the aligner.
        """
        if aligner_type == AlignerType.FUZZY_ALIGNER:
            return FuzzyAligner(**kwargs)
        elif aligner_type == AlignerType.FUZZYWUZZY_ALIGNER:
            return FuzzyWuzzyAligner(**kwargs)
        else:
            raise ValueError(
                f"Transcriber type must be one of: {[a.value for a in AlignerType]} but got {aligner_type}"
            )
