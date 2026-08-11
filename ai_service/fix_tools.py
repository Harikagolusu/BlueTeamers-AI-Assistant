import glob
import re

for file_path in glob.glob('app/agents/investigation/tools/*.py'):
    if '__init__' in file_path: continue
    with open(file_path, 'r') as f:
        content = f.read()

    match = re.search(r'name=\"(.*?)\"', content)
    if not match: continue
    tool_name = match.group(1)
    
    new_content = content.replace(
        'super().__init__()\n        self.metadata = ToolMetadata(',
        'metadata = ToolMetadata('
    )
    new_content = new_content.replace(
        '        )\n\n    async def execute',
        f'        )\n        super().__init__(name=\"{tool_name}\", metadata=metadata)\n\n    async def execute'
    )
    
    with open(file_path, 'w') as f:
        f.write(new_content)
print("done")
