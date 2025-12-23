"""Pydantic models for navigation configuration."""

from typing import Optional
import streamlit as st
from pydantic import BaseModel, Field


class NavigationPage(BaseModel):
    """Model for a single page configuration."""

    page: str = Field(..., description="Path to the page file")
    title: str = Field(..., description="Title of the page")
    icon: str = Field(..., description="Icon for the page (Material icon)")
    header: str = Field(..., description="Header text displayed on the page")
    caption: str = Field(..., description="Caption or description of the page")
    help_page: Optional[str] = Field(None, description="Path to help markdown file")
    default: Optional[bool] = Field(False, description="Whether this is the default page")
    roles: Optional[list[str]] = Field(None, description="List of roles that can access this page")


class NavigationSection(BaseModel):
    """Model for a navigation section containing multiple pages."""

    name: str = Field(..., description="Name of the navigation section")
    pages: list[NavigationPage] = Field(..., description="List of pages in this section")


class NavigationConfig(BaseModel):
    """Model for the complete navigation configuration."""

    sections: list[NavigationSection] = Field(..., description="List of navigation sections")

    @classmethod
    def from_yaml_list(cls, yaml_list: list[dict]) -> "NavigationConfig":
        """Create NavigationConfig from a list of section dictionaries."""
        return cls(sections=[NavigationSection(**section) for section in yaml_list])


@st.cache_data
def get_default_navigation_config() -> NavigationConfig:
    """Get the default navigation from navigation_config.yml."""
    import yaml
    from pathlib import Path

    config_path = Path(__file__).parent / "navigation_config.yml"
    with open(config_path, "r") as file:
        yaml_content = yaml.safe_load(file)

    return NavigationConfig.from_yaml_list(yaml_content)


navigation_config: NavigationConfig = get_default_navigation_config()
