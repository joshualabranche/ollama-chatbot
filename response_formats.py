#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 22:01:42 2025

@author: jlab
"""

from pydantic import BaseModel

class code_response(BaseModel):
    information: str
    snippet: str 
    overview: str
    execution: str