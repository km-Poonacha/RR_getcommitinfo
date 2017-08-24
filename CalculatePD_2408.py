#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 12:19:18 2017

@author: medapa

This calculates the productive deferrel using three different measures:
    PD1 = Average idle time taken for two consecutive tasks by different authors (superposed work) / 
    Average idle time taken by two consecutive contributions by different authors within a task/pullrequest (co-work) 
    
    PD2 = Average idle time taken for two consecutive tasks by different authors (superposed work) / 
    Average idle time taken between any two consecutive tasks in the project
    
    PD3 = Assess the proportion of tasks with atypical idle time (e.g., 2 standard deviations from the mean). 
"""


