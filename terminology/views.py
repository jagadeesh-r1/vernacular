from django.http import HttpResponse
from rest_framework.response import Response
from typing import List, Dict, Tuple
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

SlotValidationResult = Tuple[bool, bool, str, Dict]


@csrf_exempt
def index(request):
    return HttpResponse("hello, I don't know Frontend :( ")

@csrf_exempt
@api_view(['POST'])
def finite_values_entity(request) -> Response:
    """
    This function is used to extract the data needed to validate
    """
    data = request.data
    values = data["values"]
    supported_values = data["supported_values"]
    invalid_trigger = data["invalid_trigger"]
    key = data["key"]
    support_multiple = data["support_multiple"]
    pick_first = data["pick_first"]
    reuse = data["reuse"]
    result = validate_finite_values_entity(values,supported_values,invalid_trigger,key,support_multiple,pick_first,reuse = reuse)
    return Response(result)

@csrf_exempt
@api_view(['POST'])
def numeric_values_entity(request) -> Response:
    """
    This function is used to extract the data needed to validate
    """
    data = request.data
    values = data["values"]
    constraint = data["constraint"]
    invalid_trigger = data["invalid_trigger"]
    key = data["key"]
    support_multiple = data["support_multiple"]
    pick_first = data["pick_first"]
    var_name = data["var_name"]
    result = validate_numeric_entity(values,invalid_trigger,key,support_multiple,pick_first,constraint,var_name)
    return Response(result)


def validate_finite_values_entity(values: List[Dict], supported_values: List[str] = None,
                                invalid_trigger: str = None, key: str = None,
                                support_multiple: bool = True, pick_first: bool = False, **kwargs) -> SlotValidationResult:
    """
    Validate an entity on the basis of its value extracted.
    The method will check if the values extracted("values" arg) lies within the finite list of supported values(arg "supported_values").

    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
    :param values: Values extracted by NLU
    :param supported_values: List of supported values for the slot
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :return: a tuple of (filled, partially_filled, trigger, params)
    """
    response = {
        "filled" : None,
        "partially_filled" : None,
        "trigger" : '',
        "parameters" : {} 
    }
    params = []
    if support_multiple:
        if values:
            for value in values:
                if value["value"] in supported_values:
                    params.append(value["value"].upper())
        else:
            response["filled"] = False
            response["partially_filled"] = False
            response["trigger"] = invalid_trigger
            return response
    if len(params) == len(values):
        response["filled"] = True
        response["partially_filled"] = False
        response["trigger"] = ''

    elif len(values) > 0 and len(params) == 0:
        response["filled"] = False
        response["partially_filled"] = True
        response["trigger"] = invalid_trigger
        return response
    elif len(values) > 0 and len(params)!=len(values):
        response["filled"] = False
        response["partially_filled"] = True
        response["trigger"] = invalid_trigger
        return response

    if pick_first:
        params = " ".join(params)

    response["parameters"][key] = params

    return response

def validate_numeric_entity(values: List[Dict], invalid_trigger: str = None, key: str = None,
                            support_multiple: bool = True, pick_first: bool = False, constraint=None, var_name=None,
                            **kwargs) -> SlotValidationResult:
    """
    Validate an entity on the basis of its value extracted.
    The method will check if that value satisfies the numeric constraints put on it.
    If there are no numeric constraints, it will simply assume the value is valid.

    If there are numeric constraints, then it will only consider a value valid if it satisfies the numeric constraints.
    In case of multiple values being extracted and the support_multiple flag being set to true, the extracted values
    will be filtered so that only those values are used to fill the slot which satisfy the numeric constraint.

    If multiple values are supported and even 1 value does not satisfy the numeric constraint, the slot is assumed to be
    partially filled.

    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
    :param values: Values extracted by NLU
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :param constraint: Conditional expression for constraints on the numeric values extracted
    :param var_name: Name of the var used to express the numeric constraint
    :return: a tuple of (filled, partially_filled, trigger, params)
    """
    response = {
        "filled" : None,
        "partially_filled" : None,
        "trigger" : '',
        "parameters" : {} 
    }
    params = []
    if support_multiple:
        if values:
            for value in values:
                globals()[var_name] = value["value"]
                if eval(constraint):
                    params.append(value["value"])
        else:
            response["filled"] = False
            response["partially_filled"] = False
            response["trigger"] = invalid_trigger
            return response
    if len(params) == len(values):
        response["filled"] = True
        response["partially_filled"] = False
        response["trigger"] = ''

    elif len(values) > 0 and len(params) == 0:
        response["filled"] = False
        response["partially_filled"] = True
        response["trigger"] = invalid_trigger
        # return response
    elif len(values) > 0 and len(params)!=len(values):
        response["filled"] = False
        response["partially_filled"] = True
        response["trigger"] = invalid_trigger
        # return response

    if pick_first:
        params = params[0]

    response["parameters"][key] = params

    return response