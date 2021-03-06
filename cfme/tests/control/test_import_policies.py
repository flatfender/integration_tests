# -*- coding: utf-8 -*-
import pytest

from cfme import test_requirements
from cfme.control import import_export
from cfme.utils.path import data_path

pytestmark = [
    test_requirements.control,
    pytest.mark.tier(3)
]


@pytest.fixture(scope="module")
def import_policy_file(request):
    return data_path.join("ui/control/policies.yaml").realpath().strpath


@pytest.fixture(scope="module")
def import_invalid_yaml_file(request):
    return data_path.join("ui/control/invalid.yaml").realpath().strpath


@pytest.fixture(scope="module")
def policy_profile_collection(appliance):
    return appliance.collections.policy_profiles


@pytest.mark.meta(blockers=[1106456, 1198111], automates=[1198111])
def test_import_policies(appliance, import_policy_file):
    import_export.import_file(appliance, import_policy_file)


def test_control_import_invalid_yaml_file(appliance, import_invalid_yaml_file):
    error_message = "Error during 'Policy Import': Invalid YAML file"
    with pytest.raises(Exception, match=error_message):
        import_export.import_file(appliance, import_invalid_yaml_file)


def test_control_import_existing_policies(appliance, import_policy_file, policy_profile_collection):
    import_export.import_file(appliance, import_policy_file)
    first_import = policy_profile_collection.all_policy_profile_names
    import_export.import_file(appliance, import_policy_file)
    second_import = policy_profile_collection.all_policy_profile_names
    assert first_import == second_import
