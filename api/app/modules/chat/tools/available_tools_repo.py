# Imports
from .ContentSearchTool import ContentSearchTool
from .DatabaseSearchTool import DatabaseSearchTool
from .FinancialPlannerTool import FinancialPlannerTool
from .GoogleSearchTool import GoogleSearchTool


# Set tools
create_tool_instances = [ContentSearchTool(), DatabaseSearchTool(), FinancialPlannerTool(), GoogleSearchTool()]
all_available_tools = {tool_instance.name: tool_instance for tool_instance in create_tool_instances}

# Define default function for configuring tool
def configure_tool_schema_func(dictionary):
    """
    This function is used to get only the arguments with default values in a schema.
    """
    # Set output counter
    output = {}

    # Loop through dictionary and add only defaults
    for key, value in dictionary.items():
        if (inner_key := "default") in value.keys():
            output[key] = value[inner_key]
    
    return output