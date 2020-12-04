import matplotlib.pyplot as plt
import numpy as np
import statistics

def data_analysis(accumulated_risk_list, risk_density_full_list, risk_density_arriving_list, risk_density_sitting_list, risk_density_leaving_list):


    fig, axes = plt.subplots(nrows=2, ncols=1)

    ax0, ax1 = axes.flatten()
    
    accumulated_risk_list.sort()
    ax0.plot(accumulated_risk_list)
    ax0.set_title("Accumulated risk during restaurant visit")
    ax0.set_xlabel("Agent listed from best to worst")
    ax0.set_ylabel("Accumulated risk")

    rank = np.linspace(1,0,len(accumulated_risk_list))

    ax1.loglog(accumulated_risk_list,rank, 'b.',markersize=10,markerfacecolor='None', label='accumulated_risk_list loglog')
    ax1.set_title("Accumulated risk on loglog scale")
    ax1.set_xlabel("Accumulated risk")
    ax1.set_ylabel("cCDF")

    fig.tight_layout()


    fig, axes = plt.subplots(nrows=2, ncols=1)
    ax0, ax1 = axes.flatten()


    length = max(map(len, risk_density_full_list))
    to_plot = np.array([current_list+[0]*(length-len(current_list)) for current_list in risk_density_full_list])
    ax0.plot(to_plot.T)

    ax0.set_title('All agent')
    ax0.set_xlabel("Time steps")
    ax0.set_ylabel("Risk density")

    ax1.plot(to_plot.sum(axis=0))
    ax1.set_title('Sum of all agent')
    ax1.set_xlabel("Time steps")
    ax1.set_ylabel("Risk density")

    fig.tight_layout()

    risk_density_arriving_list_sum = sum_of_list_in_list(risk_density_arriving_list.copy())
    risk_density_sitting_list_sum = sum_of_list_in_list(risk_density_sitting_list.copy())
    risk_density_leaving_list_sum = sum_of_list_in_list(risk_density_leaving_list.copy())

    fig, axes = plt.subplots(nrows=3, ncols=1)

    ax0, ax1, ax2 = axes.flatten()

    ax0.hist(risk_density_arriving_list_sum, bins=40)
    ax0.set_ylabel("Nr of agents")
    ax0.set_xlabel("Accumulated risk density")
    ax0.set_title('risk_density_arriving')

    ax1.hist(risk_density_sitting_list_sum, bins=40)
    ax0.set_ylabel("Nr of agents")
    ax0.set_xlabel("Accumulated risk density")
    ax1.set_title('risk_density_sitting')

    ax2.hist(risk_density_leaving_list_sum, bins=40)
    ax0.set_ylabel("Nr of agents")
    ax0.set_xlabel("Accumulated risk density")
    ax2.set_title('risk_density_leaving')

    fig.tight_layout()

    print("Median risk when arriving:  ", round(statistics.median(risk_density_arriving_list_sum), 2))
    print("Median risk when sitting:   ", round(statistics.median(risk_density_sitting_list_sum), 2))
    print("Median risk when leaving:   ", round(statistics.median(risk_density_leaving_list_sum), 2))

    print("Avarage risk when arriving: ", round(statistics.mean(risk_density_arriving_list_sum), 2))
    print("Avarage risk when sitting:  ", round(statistics.mean(risk_density_sitting_list_sum), 2))
    print("Avarage risk when leaving:  ", round(statistics.mean(risk_density_leaving_list_sum), 2))

    plt.show()



def sum_of_list_in_list(input_list):
    return_list = []

    for list in input_list:
        return_list.append(sum(list))

    return return_list
