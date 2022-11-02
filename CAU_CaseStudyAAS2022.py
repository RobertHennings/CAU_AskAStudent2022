#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 20:21:53 2022

@author: Robert_Hennings
"""
#This short python script accompanies the Case Study of the Ask A Student 2022 project of the Christian-Albrechts-University of Kiel
#where I hosted the Economics and Business Administration Slot as tutor for the A-level students that were guided throughou the whole day

#import the packages used in here
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy 
import sympy 
from sympy import symbols, solve
#set resolution to retina
%config InlineBackend.figure_format = "retina"

#Construct a class that we can later use for solving the task
class CaseStudyAAS:
    def __init__(self, amount):
        #the amount should be directly set and used by the subfunctions as fixed variable
        #without any further specification
        self.amount = amount
    
    #Construct the Demand function
    def Demand_DB(self,m1,y1,m2,y2):
        """
        

        Parameters
        ----------
        m1 : float or int
            x coordinate of the first point.
        y1 : float or int
            y coordinate of the first point.
        m2 : float or int
            x coordinate of the second point.
        y2 : float or int
            y coordinate of the second point.

        Returns
        -------
        result : pd.DataFrame
            DataFrame that holds the total Demand value for the provided range of amount values.

        """
        #to set up alinear equation we need two points from which we know that they lie on the same line
        m,b = symbols ("m, b")
        eq1 = m1*m+b-y1 
        eq2 = m2*m+b-y2
        #print the solution for the parameters m and b
        print(solve((eq1,eq2), (m,b)))
        #the final linear equation 
        print("Solution for the linear equation: Y = ",solve((eq1,eq2), (m,b)).get(m), "* x +",solve((eq1,eq2), (m,b)).get(b))
        positions = []
        size = range(0,self.amount)
        #for presepcified range now apply the linear equation
        for i in range(0, self.amount):
            y = solve((eq1,eq2), (m,b)).get(m)*i+solve((eq1,eq2), (m,b)).get(b)
            positions.append(y)
        #save it in a datframe for later usage
        result = pd.DataFrame(size, columns=["Size_Stock"])
        result["PositionTotal"] = positions
        return result

        
    #the same holds for the supply equation 
    def Supply_CB(self,m1,y1,m2,y2):
        """
        

        Parameters
        ----------
        m1 : float or int
            x coordinate of the first point.
        y1 : float or int
            y coordinate of the first point.
        m2 : float or int
            x coordinate of the second point.
        y2 : float or int
            y coordinate of the second point.

        Returns
        -------
        result : pd.DataFrame
            DataFrame that holds the total Supply value for the provided range of amount values.

        """
        
        m,b = symbols ("m, b")
        eq1 = m1*m+b-y1
        eq2 = m2*m+b-y2
        print(solve((eq1,eq2), (m,b)))    
        print("Solution for the linear equation: Y = ",solve((eq1,eq2), (m,b)).get(m), "* x +",solve((eq1,eq2), (m,b)).get(b))
        positions = []
        size = range(0,self.amount)
        for i in range(0, self.amount):
            y = solve((eq1,eq2), (m,b)).get(m)*i+solve((eq1,eq2), (m,b)).get(b)
            positions.append(y)
        
        result = pd.DataFrame(size, columns=["Size_Stock"])
        result["PositionTotal"] = positions
        return result
   


    #Finally we want to find the market equilibrium, and also have it displayed as a graph
    def FindMarketEquilibrium(self,d,s):
        """
        

        Parameters
        ----------
        d : pd.DataFrame that represents the demand.
            
        s : pd.DataFrame that represents the supply.
            

        Returns
        -------
        Market equilibrium and graph of it.

        """
        market = pd.concat([d,s],axis=1)
        
        market.columns = ["Size_Stock_D", "PositionTotal_D", "Size_Stock_S", "PositionTotal_S"]
        market["Diff"] = abs(market.PositionTotal_D-market.PositionTotal_S)
        
        print("Amount x of equilibrium: ", market.Size_Stock_D[market.Diff == min(market.Diff)].values[0])
        print("Amount y of equilibrium: ", market.PositionTotal_S[market.Diff == min(market.Diff)].values[0])
        
        xvlines = market.Size_Stock_D[market.Diff == min(market.Diff)].values[0].astype("int")
        ymaxvlines = int(max(d.iloc[:,1].append(s.iloc[:,1])))
        
        yhlines = int(market.PositionTotal_S[market.Diff == min(market.Diff)].values[0]) #2582
        xmaxhlines = market.shape[0]
        
        #Plot the market and the equilibrium
        plt.plot(d.Size_Stock, d.PositionTotal, label="Nachfrage DB", color="#9A1B7D")
        plt.plot(s.Size_Stock, s.PositionTotal, label="Angebot CB",color= "grey")
        plt.legend()
        plt.title("Marktgleichgewicht Porsche-Aktie", fontsize=14)
        plt.ylabel("Gesamtpositionsgröße in €")
        plt.xlabel("Anzahl Aktien")
        plt.text(25,3100,"Amount x: "+str(market.Size_Stock_D[market.Diff == min(market.Diff)].values[0])+"\n"+"Amount y: "+str(market.PositionTotal_S[market.Diff == min(market.Diff)].values[0]),fontsize=8)
        plt.vlines(x=xvlines,ymin=0,ymax=ymaxvlines, color="black",linestyle="--")
        plt.hlines(y=yhlines,xmin=0,xmax=xmaxhlines, color="black",linestyle="--")
        plt.show()




#to use the class we first have to initialize it
Case = CaseStudyAAS(amount=51)
Case.Demand_DB(m1=25,y1=2557.50,m2=50,y2=494.00)  #provide the two points to estimate the linear euqation
Case.Supply_CB(m1=18,y1=1845,m2=28,y2=3073.84)    #provide the two points to estimate the linear euqation
#Find and plot the market equilibrium
Case.FindMarketEquilibrium(Case.Demand_DB(m1=25,y1=2557.50,m2=50,y2=494.00)  ,Case.Supply_CB(m1=18,y1=1845,m2=28,y2=3073.84))
