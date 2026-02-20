# Databricks notebook source
from main import SchemaManager

SchemaManager(dbutils.widgets.getAll()).run()