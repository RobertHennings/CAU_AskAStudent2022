#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 20:21:53 2022

@author: Robert_Hennings
"""
#This short python script accompanies the Case Study of the Ask A Student 2022 project of the Christian-Albrechts-University of Kiel
#where I hosted the Economics and Business Administration Slot as tutor for the A-level students that were guided throughou the whole day
def main():
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
            #attention: The Demand Line is declining from left to right, so the slope (the "m") needs to be negative
            m,b = symbols ("m, b") #set the slope m to a negative value 
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
            result["StockPriceDemand"] = result.PositionTotal / result.Size_Stock
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
            result["StockPriceSupply"] = result.PositionTotal / result.Size_Stock
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
            
            market.columns = ["Size_Stock_D", "PositionTotal_D","Stock_Price_D", "Size_Stock_S", "PositionTotal_S", "Stock_Price_S"]
            market["Diff"] = abs(market.PositionTotal_D-market.PositionTotal_S)
            
            print("Amount x of equilibrium: ", market.Size_Stock_D[market.Diff == min(market.Diff)].values[0])
            print("Amount y of equilibrium: ", market.PositionTotal_S[market.Diff == min(market.Diff)].values[0])
            print("Final Stock Price of Market equilibrium: ",market.PositionTotal_S[market.Diff == min(market.Diff)].values[0] / market.Size_Stock_D[market.Diff == min(market.Diff)].values[0])
            
            xvlines = market.Size_Stock_D[market.Diff == min(market.Diff)].values[0].astype("int")
            ymaxvlines = int(max(d.iloc[:,1].append(s.iloc[:,1])))
            
            yhlines = int(market.PositionTotal_S[market.Diff == min(market.Diff)].values[0]) #2582
            xmaxhlines = market.shape[0]
            
            #Plot the market and the equilibrium, watch out: here it is not a Price-Quantity Plot but a Total Position-Quantity Plot
            plt.plot(d.Size_Stock, d.PositionTotal, label="Nachfrage DB", color="#9A1B7D")
            plt.plot(s.Size_Stock, s.PositionTotal, label="Angebot CB",color= "grey")
            plt.legend()
            plt.title("Marktgleichgewicht Porsche-Aktie", fontsize=14)
            plt.ylabel("Gesamtpositionsgröße in €")
            plt.xlabel("Anzahl Aktien")
            plt.text(market.Size_Stock_D[market.Diff == min(market.Diff)].values[0]+4,market.PositionTotal_S[market.Diff == min(market.Diff)].values[0]+50,"Amount x: "+str(market.Size_Stock_D[market.Diff == min(market.Diff)].values[0])+"\n"+"Amount y: "+str(market.PositionTotal_S[market.Diff == min(market.Diff)].values[0]),fontsize=8)
            plt.vlines(x=xvlines,ymin=0,ymax=ymaxvlines, color="black",linestyle="--")
            plt.hlines(y=yhlines,xmin=0,xmax=xmaxhlines, color="black",linestyle="--")
            plt.show()
            print("Market Equilibrium Plot has loaded - Total Position-Quantity")
            
            #Next we also want to plot the usual Price-Quantity Plot as we know it because we previously looked at the Total Position Size
            #We just select the according columns in the market dataframe
            plt.plot(market.Size_Stock_D[1:], market.Stock_Price_D[1:], label = "Nachfrage DB", color="#9A1B7D" )
            plt.plot(market.Size_Stock_S[1:], market.Stock_Price_S[1:], label = "Angebot CB", color = "grey")
            plt.title("Marktgleichgewicht Porsche-Aktie", fontsize=14)
            plt.ylabel("Aktienpreis in € je Aktie")
            plt.xlabel("Anzahl Aktien")
            plt.vlines(x=market.Size_Stock_D[market.Diff == min(market.Diff)].values[0],ymin=0,ymax=int(max(market.Stock_Price_D[1:])-1), color="black",linestyle="--")
            plt.hlines(y=int(market.PositionTotal_S[market.Diff == min(market.Diff)].values[0] / market.Size_Stock_D[market.Diff == min(market.Diff)].values[0]),xmin=0,xmax=max(market.Size_Stock_D[1:]), color="black",linestyle="--")
            plt.text(market.Size_Stock_D[market.Diff == min(market.Diff)].values[0]+3,int(market.PositionTotal_S[market.Diff == min(market.Diff)].values[0] / market.Size_Stock_D[market.Diff == min(market.Diff)].values[0])+60,
                     "Amount x: " + str(market.Size_Stock_D[market.Diff == min(market.Diff)].values[0])+"\n"+"Amount y: "+str(int(market.PositionTotal_S[market.Diff == min(market.Diff)].values[0] / market.Size_Stock_D[market.Diff == min(market.Diff)].values[0])), 
                     fontsize = 8)
            plt.show()
            print("Market Equilibrium Plot has loaded - Stock Price-Quantity")
            
    #to use the class we first have to initialize it
    Case = CaseStudyAAS(amount=51)
    DemandTable = Case.Demand_DB(m1=25,y1=3251.50,m2=50,y2=2837)  #provide the two points to estimate the linear euqation
    SupplyTable = Case.Supply_CB(m1=18,y1=1845,m2=28,y2=3073.84)    #provide the two points to estimate the linear euqation
    #Find and plot the market equilibrium
    Case.FindMarketEquilibrium(Case.Demand_DB(m1=25,y1=3251.50,m2=50,y2=2837)  ,Case.Supply_CB(m1=18,y1=1845,m2=28,y2=3073.84))
    


if __name__ == "__main__":
    main()