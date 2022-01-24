import json
import logging


logging.basicConfig(format='%(asctime)s | %(levelname)-5s | %(module)s:%(lineno)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logger = logging.getLogger()


def visit(element, test, transform):
    """Visit `element` executing `transform` on keys whose `test` return True.

    Args:
        element ([dict]): the dictionary to visit
        test ([lambda]): the test lambda
        visitor ([dict]): the visit lambda
    """
    if isinstance(element, dict):
        for k, v in element.items():
            if test(k):
                logger.debug(f"Transforming {element}({k}) ...")
                return transform(v)
            else:
                logger.debug(f"Parsing obj {k} ...")
                result = visit(v, test, transform)
                if result is not None:
                    element[k] = result
    elif any(isinstance(element, t) for t in (list, tuple)):
        logger.debug(f"Parsing l/t {element} ...")
        for idx, item in enumerate(element):
            result = visit(item, test, transform)
            if result is not None:
                element[idx] = result


def handle_template(template):
    """Convert the recognized element in the template.

    Args:
        template ([type]): the template to transformed

    Returns:
        [type]: the trasnformed template
    """
    for name, resource in template.get("Resources", {}).items():
        logger.debug(f"Parsing Resource '{name}'")
        visit(resource["Properties"],
              lambda s: 'Fn::Yaml2Json' == s, json.dumps)
    return template


def lambda_handler(event, _):
    """Handle lambda events.
    """
    request_id = event["requestId"]
    fragment = event["fragment"]
    try:
        response = {
            "requestId": request_id,
            "status": "success",
            "fragment": handle_template(fragment),
        }
    except Exception as e:
        logger.error(e, exc_info=True)
        response = {
            "requestId": request_id,
            "status": "failure",
            "fragment": fragment,
        }
    return response
