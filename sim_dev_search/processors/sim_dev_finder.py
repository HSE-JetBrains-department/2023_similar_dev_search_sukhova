from collections import Counter, defaultdict
from typing import Any, Dict, List, Tuple

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimilarDevelopersFinder:
    """
    Class that finds similar developers.
    """

    LANGUAGE_FIELD = "languages"
    VARIABLES_FIELD = "variables"

    @staticmethod
    def _get_developers_dataframe(developers_info: Dict[str, Any]) -> pd.DataFrame:
        """
        Get pandas dataframe from python dictionary.
        :param developers_info: Dict with information about developers.
        :return: Pandas dataframe with information about developers.
        """
        vectorizer = DictVectorizer(dtype=int, sparse=False)
        dev_matrix = vectorizer.fit_transform(developers_info.values())

        dev_df = pd.DataFrame(dev_matrix, columns=vectorizer.feature_names_, index=list(developers_info.keys()))
        dev_df.fillna(0, inplace=True)
        return dev_df

    def _get_developers_info_for_df(self, developers_info: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get processed dict with information about developers to create pandas dataframe.
        :param developers_info: Dict with information about developers.
        :return: Processed dict with information about developers.
        """
        developers_info_for_df = defaultdict(Counter)
        for dev_email, repos_info in developers_info.items():
            for repo_name, repo_info in repos_info.items():
                developers_info_for_df[dev_email] += Counter(
                    {**repo_info[self.VARIABLES_FIELD], **repo_info[self.LANGUAGE_FIELD]}
                )
        return developers_info_for_df

    @staticmethod
    def _get_top_params(
        developer_info: Dict[str, Dict[str, Any]],
        parameters_field: str,
        parameters_top_size: int,
    ) -> Dict[str, int]:
        """
        Get top of parameters used by developer.
        :param developer_info: Dict with information about developers.
        :param parameters_field: Name of field to get top parameters.
        :param parameters_top_size: Size of parameters used by similar developers top.
        :return: Top of parameters used by developer.
        """
        params_frequencies = Counter()
        for repo_info in developer_info.values():
            for param_name, param_frequency in repo_info[parameters_field].items():
                params_frequencies[param_name] += param_frequency
        return dict(params_frequencies.most_common(parameters_top_size))

    def _get_similar_developers_info(
        self,
        similarity_info: List[Tuple[str, float]],
        developers_info: Dict[str, Dict[str, Any]],
        parameters_top_size: int,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get information about top parameters used by similar developers.
        :param similarity_info: Dict with information about similar developers.
        :param developers_info: Dict with information about developers.
        :param parameters_top_size: Size of parameters used by similar developers top.
        :return: Dict with information about top parameters used by similar developers.
        """
        similar_developers_info: Dict[str, Dict[str, Any]] = {}
        for user_email, user_score in similarity_info:
            similar_developers_info[user_email] = {
                "similarity_score": user_score,
                "top_languages": self._get_top_params(
                    developer_info=developers_info[user_email],
                    parameters_field=self.LANGUAGE_FIELD,
                    parameters_top_size=parameters_top_size,
                ),
                "top_identifiers": self._get_top_params(
                    developer_info=developers_info[user_email],
                    parameters_field=self.VARIABLES_FIELD,
                    parameters_top_size=parameters_top_size,
                ),
            }
        return similar_developers_info

    def get_similar_developers(
        self,
        user_email: str,
        developers_info: Dict[str, Dict[str, Any]],
        similar_developers_number: int = 15,
        parameters_top_size: int = 15,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get similar developers for given developer.
        :param user_email: Email of developer to find similar.
        :param developers_info: Dict with information about developers.
        :param similar_developers_number: Number of similar developers to find.
        :param parameters_top_size: Size of parameters used by similar developers top.
        :return: Similar developers emails with similarity scores.
        """
        developers_info_for_df = self._get_developers_info_for_df(developers_info)
        developers_df = self._get_developers_dataframe(developers_info_for_df)

        dev_similarity = cosine_similarity(
            developers_df[developers_df.index != user_email], developers_df[developers_df.index == user_email]
        ).reshape(-1)
        res_similarity = list(zip(developers_df[developers_df.index != user_email].index, dev_similarity))
        res_similarity_sorted = sorted(res_similarity, key=lambda res: res[1], reverse=True)[:similar_developers_number]
        res_similarity_info = self._get_similar_developers_info(
            similarity_info=res_similarity_sorted,
            developers_info=developers_info,
            parameters_top_size=parameters_top_size,
        )
        return res_similarity_info
