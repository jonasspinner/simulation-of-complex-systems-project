import matplotlib.pyplot as plt
import numpy as np
import statistics

def data_analysis(accumulated_risk_list, risk_density_full_list, risk_density_arriving_list, risk_density_sitting_list, risk_density_leaving_list):

    accumulated_risk_list.sort()
    plt.plot(accumulated_risk_list)
    plt.title("Accumulated drops during restaurant visit")
    plt.xlabel("Agent listed from best to worst")
    plt.ylabel("Accumulated drops")
    plt.show()

    for droplets_list in risk_density_full_list:
        plt.plot(droplets_list)

    plt.title('All agent to leave restaurant')
    plt.xlabel("Time steps")
    plt.ylabel("Drop in area during time step")
    plt.show()

    risk_density_arriving_list_sum = sum_of_list_in_list(risk_density_arriving_list.copy())
    risk_density_sitting_list_sum = sum_of_list_in_list(risk_density_sitting_list.copy())
    risk_density_leaving_list_sum = sum_of_list_in_list(risk_density_leaving_list.copy())

    maxnr = max(accumulated_risk_list)

    max_arriving = max(risk_density_arriving_list_sum)
    max_sitting = max(risk_density_sitting_list_sum)
    max_leaving = max(risk_density_leaving_list_sum)

    hist, bin_edges = np.histogram(accumulated_risk_list, density=True, bins=np.arange(0,maxnr,maxnr/10))

    plt.plot(hist)
    plt.ylim((0, max(hist)))
    plt.show()

    hist_arriving, bin_edges_arriving = np.histogram(risk_density_arriving_list_sum, density=True, bins=np.arange(0,max_arriving,max_arriving/10))
    hist_sitting, bin_edges_sitting = np.histogram(risk_density_sitting_list_sum, density=True, bins=np.arange(0,max_sitting,max_sitting/10))
    hist_leaving, bin_edges_leaving = np.histogram(risk_density_leaving_list_sum, density=True, bins=np.arange(0,max_leaving,max_leaving/10))

    for droplets_list in risk_density_arriving_list_sum:
        plt.plot(droplets_list)

    plt.plot(hist_arriving)
    plt.ylim((0, max(hist_arriving)))
    plt.show()

    plt.plot(hist_sitting)
    plt.ylim((0, max(hist_sitting)))
    plt.show()

    plt.plot(hist_leaving)
    plt.ylim((0, max(hist_leaving)))
    plt.show()

    print("Median risk when arriving: ", statistics.median(risk_density_arriving_list_sum))
    print("Median risk when sitting: ", statistics.median(risk_density_sitting_list_sum))
    print("Median risk when leaving: ", statistics.median(risk_density_leaving_list_sum))

    print("Avarage risk when arriving: ", statistics.mean(risk_density_arriving_list_sum))
    print("Avarage risk when sitting: ", statistics.mean(risk_density_sitting_list_sum))
    print("Avarage risk when leaving: ", statistics.mean(risk_density_leaving_list_sum))


def sum_of_list_in_list(input_list):
    return_list = []

    for list in input_list:
        return_list.append(sum(list))

    return return_list
