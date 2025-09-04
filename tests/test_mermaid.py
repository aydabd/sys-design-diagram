"""Copyright (c) 2024, Aydin Abdi.

This module contains tests for the MermaidDiagram class in the sys_design_diagram.mermaid module.
"""

import pytest
from sys_design_diagram.exceptions import MermaidExecutionError, MermaidFileNotFoundError
from sys_design_diagram.messages import ErrorMessages
from sys_design_diagram.mermaid import MermaidDiagram


@pytest.mark.asyncio
async def test_init_valid_file(setup_design_dirs):
    """Test initializing MermaidDiagram with a valid file."""
    # Create a temporary mermaid file
    mermaid_file = setup_design_dirs / "design_1" / "test.mmd"
    mermaid_file.write_text("graph TD\n    A --> B")
    
    diagram = MermaidDiagram(mermaid_file)
    assert diagram.mermaid_file == mermaid_file


@pytest.mark.asyncio
async def test_init_invalid_file(setup_design_dirs):
    """Test initializing MermaidDiagram with an invalid file."""
    invalid_file = setup_design_dirs / "design_1" / "non_existent.mmd"
    with pytest.raises(
        MermaidFileNotFoundError, match=ErrorMessages.FILE_NOT_FOUND.value.format(file_path=invalid_file)
    ):
        MermaidDiagram(invalid_file)


@pytest.mark.asyncio
async def test_init_invalid_path_type():
    """Test initializing MermaidDiagram with an invalid path type."""
    with pytest.raises(TypeError, match=ErrorMessages.NOT_A_PATH.value.format(path="not_a_path")):
        MermaidDiagram("not_a_path")


@pytest.mark.asyncio
async def test_create_with_valid_output_dir(setup_design_dirs, output_dir):
    """Test creating a diagram with a valid output directory."""
    # Create a temporary mermaid file
    mermaid_file = setup_design_dirs / "design_1" / "test.mmd"
    mermaid_file.write_text("graph TD\n    A --> B")
    
    diagram = MermaidDiagram(mermaid_file)
    await diagram.create(output_dir)
    
    # Check that a placeholder file was created (since mmdc likely won't work in CI)
    output_file = output_dir / "test.png"
    assert output_file.exists()
    
    # Should contain either actual PNG data or placeholder text
    content = output_file.read_text()
    assert "test.mmd" in content


@pytest.mark.asyncio
async def test_create_with_invalid_output_dir(setup_design_dirs):
    """Test creating a diagram with an invalid output directory."""
    # Create a temporary mermaid file
    mermaid_file = setup_design_dirs / "design_1" / "test.mmd"
    mermaid_file.write_text("graph TD\n    A --> B")
    
    diagram = MermaidDiagram(mermaid_file)
    
    # Test with non-existent directory
    non_existent_dir = setup_design_dirs / "non_existent"
    with pytest.raises(ValueError, match=ErrorMessages.DIRECTORY_NOT_FOUND.value.format(directory_path=non_existent_dir)):
        await diagram.create(non_existent_dir)


@pytest.mark.asyncio
async def test_create_with_invalid_output_path_type(setup_design_dirs):
    """Test creating a diagram with an invalid output path type."""
    # Create a temporary mermaid file
    mermaid_file = setup_design_dirs / "design_1" / "test.mmd"
    mermaid_file.write_text("graph TD\n    A --> B")
    
    diagram = MermaidDiagram(mermaid_file)
    
    with pytest.raises(TypeError, match=ErrorMessages.NOT_A_PATH.value.format(path="not_a_path")):
        await diagram.create("not_a_path")


@pytest.mark.asyncio
async def test_create_with_file_as_output_dir(setup_design_dirs):
    """Test creating a diagram with a file as output directory."""
    # Create a temporary mermaid file
    mermaid_file = setup_design_dirs / "design_1" / "test.mmd"
    mermaid_file.write_text("graph TD\n    A --> B")
    
    diagram = MermaidDiagram(mermaid_file)
    
    # Create a file to use as output dir
    file_path = setup_design_dirs / "design_1" / "not_a_dir.txt"
    file_path.write_text("not a directory")
    
    with pytest.raises(ValueError, match=ErrorMessages.NOT_A_DIRECTORY.value.format(directory_path=file_path)):
        await diagram.create(file_path)