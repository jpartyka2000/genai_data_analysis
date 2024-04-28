from flufl.enum import Enum


class DimensionCompositionType(Enum):
    GZDF = 1
    PPI1 = 2
    PPI2 = 3
    UNKNOWN = 4


class EqualityOperation(Enum):
    GREATER_THAN = 1
    LESS_THAN = 2
    EQUAL = 3
    GREATER_THAN_EQUAL = 4
    LESS_THAN_EQUAL = 5
    NOT_EQUAL = 6

# todo: add more dimensions to the list
class Dimension(Enum):
    VERBAL_REASONING = 30
    NUMERICAL_REASONING = 31
    MENTAL_FLEXIBILITY = 32


class SpreadsheetColumnExport(Enum):
    EXPORT_NAME = 0
    SSN = 1
    CANDIDATE_ID = 2
    ASSESSMENT_SCORES = 3
    POSITION_INFO = 4
    TEST_INFO = 5
    HIRE_DATE = 6
    HIRE_LOCATION = 7
    BIOGRAPHICAL_DATA = 8
    QUALITY_CONTROL = 9
    ASSESSMENT_COMPLETE_DATE = 10
    TEST_COMPLETE_DATE = 11
    PROFILE_FIT_SCORES = 12
    COMPANY_CANDIDATE_ID = 13
    COMPANY_CANDIDATE_CODE = 14
    PARTNER_CANDIDATE_CODE = 15


class Ethnicity(Enum):
    DO_NOT_WISH_TO_SELF_IDENTIFY = 0
    WHITE = 1
    HISPANIC = 2
    AFRICAN_AMERICAN = 3
    ASIAN = 4
    HAWAIIAN_OR_PACIFIC_ISLANDER = 5
    AMERICAN_INDIAN = 6
    OTHER = 7


class QualityControlMetric(Enum):
    PMA_MINUTES = 1
    PPI_TOTAL_ITEM_MINUTES = 2
    PPI_MINUTES = 3
    FALSIFICATION = 4
    CONSISTENCY = 5
    CLICK_THROUGH = 6
    SEQUENCE = 7
    LCS_LENGTH = 8
    INCONSISTENCY = 9
    DISTORTION = 10


class MatchingMethodType(Enum):
    FIRST_NAME_LAST_NAME = 1
    EMAIL_FIRST_NAME_LAST_NAME = 2
    EMAIL = 3
    LAST_NAME_FIRST_INITIAL = 4
    FULL_SSN = 5
    LAST_NAME_AND_LAST_SIX_SSN = 6
    LAST_NAME_AND_LAST_FOUR_SSN = 7
    LAST_NAME = 8
    FIRST_NAME_MIDDLE_NAME_LAST_NAME = 9
    LAST_SIX_SSN = 10
    LAST_FOUR_SSN = 11
    FIRST_THREE_OF_FIRST_AND_FIRST_THREE_OF_LAST = 12
    CANDIDATE_ID = 13
    EMPLOYEE_ID = 14
    CUSTOM = 15
    FIRST_NAME = 16
    MIDDLE_NAME = 17
    DATE_OF_BIRTH = 18
    PHONE_NUMBER = 19
    CUSTOM_SSN = 20
    LAST_NAME_AND_BIRTH_YEAR = 21
    LAST_NAME_AND_DATE_OF_BIRTH = 22
    FIRST_NAME_LAST_NAME_LAST_FOUR_SSN = 23
    LAST_NAME_AND_FIRST_INITIAL_AND_LAST_FOUR_SSN = 24
    FIRST_THREE_OF_FIRST_AND_FIRST_THREE_OF_LAST_AND_LAST_FOUR_SSN = 25
    COMPANY_CANDIDATE_ID = 26
    COMPANY_CANDIDATE_CODE = 27
    PARTNER_CANDIDATE_CODE = 28


class CompleteOrIncomplete(Enum):
    COMPLETE = 1
    INCOMPLETE = 2


class GroupByHavingCount(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR_OR_MORE = 4


class CandidateTestStatus(Enum):
    NOT_STARTED = 1
    IN_PROCESS = 2
    TIME_EXPIRED = 3
    INVALID = 4
    COMPLETE = 5


class ConstantsMisc():
    SECONDS_PER_MINUTE = 60
    MILLISECONDS_PER_SECOND = 1000
    MILLISECONDS_PER_MINUTE = SECONDS_PER_MINUTE * MILLISECONDS_PER_SECOND

    ACTIVE_QUALITY_CONTROL_METRICS = [QualityControlMetric.PPI_TOTAL_ITEM_MINUTES,
                                      QualityControlMetric.PPI_MINUTES,
                                      QualityControlMetric.FALSIFICATION,
                                      QualityControlMetric.CONSISTENCY,
                                      QualityControlMetric.CLICK_THROUGH,
                                      QualityControlMetric.SEQUENCE,
                                      QualityControlMetric.LCS_LENGTH]


class ConstantsTests():
    TEST_GROUP_ID_PMA = 1
    TEST_GROUP_ID_DF240 = 3
    TEST_GROUP_ID_DFR = 4
    TEST_GROUP_ID_GZTS = 6
    TEST_GROUP_ID_GZTSR = 7
    TEST_GROUP_ID_PPI1 = 12
    TEST_GROUP_ID_PPI2 = 21


class ConstantsMatching():
    CANDIDATE_DATA_ITEMS_CANDIDATE_ID_INDEX = 0
    CANDIDATE_DATA_ITEMS_COMPANY_CANDIDATE_ID_INDEX = 1
    CANDIDATE_DATA_ITEMS_FIRST_NAME_INDEX = 2
    CANDIDATE_DATA_ITEMS_LAST_NAME_INDEX = 3
    CANDIDATE_DATA_ITEMS_EMAIL_INDEX = 4
    CANDIDATE_DATA_ITEMS_SSN_INDEX = 5
    CANDIDATE_DATA_ITEMS_EMPLOYEE_ID_INDEX = 6
    CANDIDATE_DATA_ITEMS_BIRTH_YEAR_INDEX = 7
    CANDIDATE_DATA_ITEMS_COMPANY_CANDIDATE_CODE_INDEX = 8
    CANDIDATE_DATA_ITEMS_PARTNER_CANDIDATE_CODE_INDEX = 9
    CANDIDATE_DATA_ITEMS_DIMENSION_VALUE_STATUS_INDEX_2_5 = 10
    CANDIDATE_DATA_ITEMS_SPREADSHEET_ROW_NUM_INDEX_2_5 = 11
    CANDIDATE_DATA_ITEMS_GIVEN_FIRST_NAME_INDEX_2_5 = 12
    CANDIDATE_DATA_ITEMS_GIVEN_LAST_NAME_INDEX_2_5 = 13
    CANDIDATE_DATA_ITEMS_GIVEN_EMAIL_INDEX_2_5 = 14
    CANDIDATE_DATA_ITEMS_GIVEN_SSN_INDEX_2_5 = 15
    CANDIDATE_DATA_ITEMS_GIVEN_COMPANY_CANDIDATE_ID_INDEX = 16
    CANDIDATE_DATA_ITEMS_GIVEN_COMPANY_CANDIDATE_CODE_INDEX = 17
    CANDIDATE_DATA_ITEMS_GIVEN_PARTNER_CANDIDATE_CODE_INDEX = 18
    CANDIDATE_DATA_ITEMS_MATCHING_METHOD_TYPE_INDEX = 19
    CANDIDATE_DATA_ITEMS_GROUP_BY_HAVING_COUNT_INDEX = 20
    CANDIDATE_DATA_ITEMS_COUNT_2_5 = 21

    CSV_LABEL_MATCHED_HOW = "Matched How?"
    CSV_LABEL_COMPLETE_OR_INCOMPLETE = "Complete or Incomplete?"
    CSV_LABEL_GIVEN_FIRST_NAME = "Given First Name"
    CSV_LABEL_GIVEN_MIDDLE_NAME = "Given Middle Name"
    CSV_LABEL_GIVEN_LAST_NAME = "Given Last Name"
    CSV_LABEL_GIVEN_EMAIL = "Given Email"
    CSV_LABEL_GIVEN_SSN = "Given SSN"
    CSV_LABEL_GIVEN_EMPLOYEE_ID = "Given Employee ID"
    CSV_LABEL_GIVEN_DOB = "Given DoB"
    CSV_LABEL_GIVEN_BIRTH_YEAR = "Given Birth Year"
    CSV_LABEL_GIVEN_PHONE_NUMBER = "Given Phone Number"
    CSV_LABEL_GIVEN_COMPANY_CANDIDATE_ID = "Given Company Candidate ID"
    CSV_LABEL_GIVEN_COMPANY_CANDIDATE_CODE = "Given Company Candidate Code"
    CSV_LABEL_GIVEN_PARTNER_CANDIDATE_CODE = "Given Partner Candidate Code"

    CSV_LABEL_MATCHED_CANDIDATE_ID = "Candidate ID"
    CSV_LABEL_MATCHED_FIRST_NAME = "Matched First Name"
    CSV_LABEL_MATCHED_MIDDLE_NAME = "Matched Middle Name"
    CSV_LABEL_MATCHED_LAST_NAME = "Matched Last Name"
    CSV_LABEL_MATCHED_EMAIL = "Matched Email"
    CSV_LABEL_MATCHED_SSN = "Matched SSN"
    CSV_LABEL_MATCHED_BIRTH_YEAR = "Matched Birth Year"
    CSV_LABEL_MATCHED_DOB = "Matched DOB"
    CSV_LABEL_MATCHED_EMPLOYEE_ID = "Matched Employee ID"
    CSV_LABEL_MATCHED_PHONE_NUMBER = "Matched Phone Number"
    CSV_LABEL_MATCHED_COMPANY_CANDIDATE_ID = "Matched Company Candidate ID"
    CSV_LABEL_MATCHED_COMPANY_CANDIDATE_CODE = "Matched Company Candidate Code"
    CSV_LABEL_MATCHED_PARTNER_CANDIDATE_CODE = "Matched Partner Candidate Code"

    CANDIDATE_DATA_ITEMS_SEPARATOR = '|'

    DEFAULT_NONE_OPTION = -1


class ConstantsProfiles():
    DEFAULT_QC_PMA_TIME = 3.0
    DEFAULT_QC_TIME_PPI1 = 14.51
    DEFAULT_QC_TIME_PPI2 = 12.96
    DEFAULT_QC_TIME_NO_FLAG = 0
    DEFAULT_QC_ITEM_TIME_PPI1 = 12.42
    DEFAULT_QC_ITEM_TIME_PPI2 = 11.12
    DEFAULT_QC_ITEM_TIME_NO_FLAG = 0
    DEFAULT_QC_CONSISTENCY_PPI1 = 57.5
    DEFAULT_QC_CONSISTENCY_PPI2 = 66.67
    DEFAULT_QC_CONSISTENCY_NO_FLAG = 100.0
    DEFAULT_QC_INCONSISTENCY_PPI1 = 40
    DEFAULT_QC_INCONSISTENCY_NO_FLAG = 100
    DEFAULT_QC_CLICK_THROUGH_PPI1 = 72.17
    DEFAULT_QC_CLICK_THROUGH_PPI2 = 66.42
    DEFAULT_QC_CLICK_THROUGH_NO_FLAG = 100
    DEFAULT_QC_SEQUENCE_PPI1 = 1
    DEFAULT_QC_SEQUENCE_PPI2 = 2
    DEFAULT_QC_SEQUENCE_NO_FLAG = 20
    DEFAULT_QC_LCS_LENGTH_PPI1 = 13
    DEFAULT_QC_LCS_LENGTH_PPI2 = 17
    DEFAULT_QC_LCS_LENGTH_NO_FLAG = 200
    DEFAULT_QC_FALSIFICATION_PPI1 = 95.5
    DEFAULT_QC_FALSIFICATION_PPI2 = 75.0
    DEFAULT_QC_FALSIFICATION_NO_FLAG = 100.0
    DEFAULT_QC_DISTORTION_PPI1 = 8
    DEFAULT_QC_DISTORTION_PPI2 = 10
    DEFAULT_QC_DISTORTION_NO_FLAG = 10


def get_matched_how(matching_method_type, group_by_having_count):
    matched_how = ''
    if matching_method_type is not None:
        matched_how += matching_method_type.name.title().replace("_", " ")

    if group_by_having_count is not None:
        if group_by_having_count.value == GroupByHavingCount.ONE.value:
            matched_how += ' - 1 Result'
        elif group_by_having_count.value == GroupByHavingCount.FOUR_OR_MORE.value:
            matched_how += ' - 4+ Results'
        else:
            matched_how += ' - ' + str(group_by_having_count.value) + ' Results'

    return matched_how


def get_boolean_value(boolean_string):
    boolean_value = False
    if boolean_string == 'Y' or boolean_string == 'y' or boolean_string == 1 or boolean_string == 'yes' or \
                    boolean_string == 'Yes' or boolean_string == 'True' or boolean_string == 'true':
        boolean_value = True

    return boolean_value


def get_default_cutoffs(dimension_composition_type):

    time_cutoff_PMA_minutes = ConstantsProfiles.DEFAULT_QC_PMA_TIME

    if dimension_composition_type == DimensionCompositionType.PPI2.value:

        time_cutoff_PPI_minutes = ConstantsProfiles.DEFAULT_QC_TIME_PPI2
        item_time_cutoff_PPI_minutes = ConstantsProfiles.DEFAULT_QC_ITEM_TIME_PPI2
        consistency_percentage_cutoff = ConstantsProfiles.DEFAULT_QC_CONSISTENCY_PPI2 / 100.0
        click_through_percentage_cutoff = ConstantsProfiles.DEFAULT_QC_CLICK_THROUGH_PPI2 / 100.0
        sequence_cutoff = ConstantsProfiles.DEFAULT_QC_SEQUENCE_PPI2
        lcs_length_cutoff = ConstantsProfiles.DEFAULT_QC_LCS_LENGTH_PPI2
        falsification_cutoff = ConstantsProfiles.DEFAULT_QC_FALSIFICATION_PPI2
        inconsistency_cutoff = ConstantsProfiles.DEFAULT_QC_INCONSISTENCY_NO_FLAG
        distortion_cutoff = ConstantsProfiles.DEFAULT_QC_DISTORTION_PPI2

    elif dimension_composition_type == DimensionCompositionType.PPI1.value:

        time_cutoff_PPI_minutes = ConstantsProfiles.DEFAULT_QC_TIME_PPI1
        item_time_cutoff_PPI_minutes = ConstantsProfiles.DEFAULT_QC_ITEM_TIME_PPI1
        consistency_percentage_cutoff = ConstantsProfiles.DEFAULT_QC_CONSISTENCY_PPI1 / 100.0
        click_through_percentage_cutoff = ConstantsProfiles.DEFAULT_QC_CLICK_THROUGH_PPI1 / 100.0
        sequence_cutoff = ConstantsProfiles.DEFAULT_QC_SEQUENCE_PPI1
        lcs_length_cutoff = ConstantsProfiles.DEFAULT_QC_LCS_LENGTH_PPI1
        falsification_cutoff = ConstantsProfiles.DEFAULT_QC_FALSIFICATION_PPI1
        inconsistency_cutoff = ConstantsProfiles.DEFAULT_QC_INCONSISTENCY_PPI1
        distortion_cutoff = ConstantsProfiles.DEFAULT_QC_DISTORTION_PPI1

    elif dimension_composition_type == DimensionCompositionType.GZDF.value:

        time_cutoff_PPI_minutes = ConstantsProfiles.DEFAULT_QC_TIME_NO_FLAG
        item_time_cutoff_PPI_minutes = ConstantsProfiles.DEFAULT_QC_ITEM_TIME_NO_FLAG
        consistency_percentage_cutoff = ConstantsProfiles.DEFAULT_QC_CONSISTENCY_NO_FLAG / 100.0
        click_through_percentage_cutoff = ConstantsProfiles.DEFAULT_QC_CLICK_THROUGH_NO_FLAG / 100.0
        sequence_cutoff = ConstantsProfiles.DEFAULT_QC_SEQUENCE_NO_FLAG
        lcs_length_cutoff = ConstantsProfiles.DEFAULT_QC_LCS_LENGTH_NO_FLAG
        falsification_cutoff = ConstantsProfiles.DEFAULT_QC_FALSIFICATION_NO_FLAG
        inconsistency_cutoff = ConstantsProfiles.DEFAULT_QC_INCONSISTENCY_NO_FLAG
        distortion_cutoff = ConstantsProfiles.DEFAULT_QC_DISTORTION_NO_FLAG
    else:
        raise Exception("Dimension Composition Type  [" + str(dimension_composition_type) + "] is not supported")

    default_cutoff_builder = {}
    default_cutoff_builder[QualityControlMetric.PMA_MINUTES.value] = time_cutoff_PMA_minutes
    default_cutoff_builder[QualityControlMetric.PPI_TOTAL_ITEM_MINUTES.value] = item_time_cutoff_PPI_minutes
    default_cutoff_builder[QualityControlMetric.PPI_MINUTES.value] = time_cutoff_PPI_minutes
    default_cutoff_builder[QualityControlMetric.FALSIFICATION.value] = falsification_cutoff
    default_cutoff_builder[QualityControlMetric.CONSISTENCY.value] = consistency_percentage_cutoff
    default_cutoff_builder[QualityControlMetric.CLICK_THROUGH.value] = click_through_percentage_cutoff
    default_cutoff_builder[QualityControlMetric.SEQUENCE.value] = sequence_cutoff
    default_cutoff_builder[QualityControlMetric.LCS_LENGTH.value] = lcs_length_cutoff
    default_cutoff_builder[QualityControlMetric.INCONSISTENCY.value] = inconsistency_cutoff
    default_cutoff_builder[QualityControlMetric.DISTORTION.value] = distortion_cutoff

    return default_cutoff_builder


def get_default_quality_control_flagged(dimension_composition_type, candidate_QC_metrics):

    default_cutoff = get_default_cutoffs(dimension_composition_type)
    candidate_QC_metrics_flagged = {}
    num_flagged = 0

    for key, value in candidate_QC_metrics.iteritems():
        if key == QualityControlMetric.PMA_MINUTES.value:
            num_flagged, flagged = get_flagged_state(default_cutoff[key], value, num_flagged, EqualityOperation.GREATER_THAN.value)
            candidate_QC_metrics_flagged[key] = flagged
        elif key == QualityControlMetric.PPI_TOTAL_ITEM_MINUTES.value:
            num_flagged, flagged = get_flagged_state(default_cutoff[key], value, num_flagged, EqualityOperation.GREATER_THAN_EQUAL.value)
            candidate_QC_metrics_flagged[key] = flagged
        elif key == QualityControlMetric.PPI_MINUTES.value:
            num_flagged, flagged = get_flagged_state(default_cutoff[key], value, num_flagged, EqualityOperation.GREATER_THAN_EQUAL.value)
            candidate_QC_metrics_flagged[key] = flagged
        elif key == QualityControlMetric.FALSIFICATION.value:
            num_flagged, flagged = get_flagged_state(default_cutoff[key], value, num_flagged, EqualityOperation.LESS_THAN_EQUAL.value)
            candidate_QC_metrics_flagged[key] = flagged
        elif key == QualityControlMetric.CONSISTENCY.value:
            num_flagged, flagged = get_flagged_state(default_cutoff[key], value, num_flagged, EqualityOperation.GREATER_THAN_EQUAL.value)
            candidate_QC_metrics_flagged[key] = flagged
        elif key == QualityControlMetric.CLICK_THROUGH.value:
            num_flagged, flagged = get_flagged_state(default_cutoff[key], value, num_flagged, EqualityOperation.LESS_THAN_EQUAL.value)
            candidate_QC_metrics_flagged[key] = flagged
        elif key == QualityControlMetric.SEQUENCE.value:
            num_flagged, flagged = get_flagged_state(default_cutoff[key], value, num_flagged, EqualityOperation.LESS_THAN_EQUAL.value)
            candidate_QC_metrics_flagged[key] = flagged
        elif key == QualityControlMetric.LCS_LENGTH.value:
            num_flagged, flagged = get_flagged_state(default_cutoff[key], value, num_flagged, EqualityOperation.LESS_THAN_EQUAL.value)
            candidate_QC_metrics_flagged[key] = flagged
        elif key == QualityControlMetric.INCONSISTENCY.value:
            num_flagged, flagged = get_flagged_state(default_cutoff[key], value, num_flagged, EqualityOperation.LESS_THAN_EQUAL.value)
            candidate_QC_metrics_flagged[key] = flagged
        elif key == QualityControlMetric.DISTORTION.value:
            num_flagged, flagged = get_flagged_state(default_cutoff[key], value, num_flagged, EqualityOperation.LESS_THAN_EQUAL.value)
            candidate_QC_metrics_flagged[key] = flagged

    return candidate_QC_metrics_flagged, num_flagged


def get_flagged_state(cutoff, value, num_flagged, equality_operation):
    flagged = 0

    if value is not None:
        if equality_operation == EqualityOperation.GREATER_THAN.value:
            if cutoff > value:
                flagged = 1
                num_flagged += 1
        elif equality_operation == EqualityOperation.LESS_THAN.value:
            if cutoff < value:
                flagged = 1
                num_flagged += 1
        elif equality_operation == EqualityOperation.GREATER_THAN_EQUAL.value:
            if cutoff >= value:
                flagged = 1
                num_flagged += 1
        elif equality_operation == EqualityOperation.LESS_THAN_EQUAL.value:
            if cutoff <= value:
                flagged = 1
                num_flagged += 1
    else:
        flagged = ''

    return num_flagged, flagged

