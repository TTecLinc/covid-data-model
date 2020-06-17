import os
import json
import pandas as pd
from pyseir import cli
from pyseir.utils import get_run_artifact_path, RunArtifact
import libs.datasets.can_model_output_schema as schema
import logging

import pytest

# _logger = logging.getLogger(__name__)

# turns all warnings into errors for this module
pytestmark = pytest.mark.filterwarnings("error")


def test__pyseir_end_to_end():
    # This covers a lot of edge cases.
    # cli._run_all(state='Idaho')
    logging.info("starting test")
    cli._build_all_for_states(states=["Idaho"], generate_reports=False)
    path = get_run_artifact_path("16001", RunArtifact.WEB_UI_RESULT).replace(
        "__INTERVENTION_IDX__", "2"
    )
    assert os.path.exists(path)

    with open(path) as f:
        output = json.load(f)

    output = pd.DataFrame(output)
    print("output df")
    print(output)
    rt_col = schema.CAN_MODEL_OUTPUT_SCHEMA.index(schema.RT_INDICATOR)
    print("rt_col")
    print(rt_col)
    print("are any rt_col greater than zero?")
    print((output[rt_col].astype(float) > 0).any())
    print("how many entries are greater than 6?")
    print((output.loc[output[rt_col].astype(float).notnull(), rt_col].astype(float) < 6).all())

    assert (output[rt_col].astype(float) > 0).any()
    assert (output.loc[output[rt_col].astype(float).notnull(), rt_col].astype(float) < 6).all()
