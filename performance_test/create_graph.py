import numpy as np
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt

divider = 1

BITCOIN_data = np.genfromtxt('performance_test/data/BITCOIN.csv', delimiter=',')
# remove nan values and limit to first 1000 samples and divide by 1000 to get seconds
BITCOIN_data = BITCOIN_data[~np.isnan(BITCOIN_data)][0:1000]/divider
ETHEREUM_data = np.genfromtxt('performance_test/data/ETHEREUM.csv', delimiter=',')
ETHEREUM_data = ETHEREUM_data[~np.isnan(ETHEREUM_data)][0:1000]/divider
MULTICHAIN_data = np.genfromtxt('performance_test/data/MULTICHAIN.csv', delimiter=',')
MULTICHAIN_data = MULTICHAIN_data[~np.isnan(MULTICHAIN_data)][0:1000]/divider
STELLAR_data = np.genfromtxt('performance_test/data/STELLAR.csv', delimiter=',')
STELLAR_data = STELLAR_data[~np.isnan(STELLAR_data)][0:1000]/divider
EOS_data = np.genfromtxt('performance_test/data/EOS.csv', delimiter=',')
EOS_data = EOS_data[~np.isnan(EOS_data)][0:1000]/divider
IOTA_data = np.genfromtxt('performance_test/data/IOTA.csv', delimiter=',')
IOTA_data = IOTA_data[~np.isnan(IOTA_data)][0:1000]/divider
HYPERLEDGER_data = np.genfromtxt('performance_test/data/HYPERLEDGER.csv', delimiter=',')
HYPERLEDGER_data = HYPERLEDGER_data[~np.isnan(
	HYPERLEDGER_data)][0:1000]/divider
POSTGRES_data = np.genfromtxt('performance_test/data/POSTGRES.csv', delimiter=',')
POSTGRES_data = POSTGRES_data[~np.isnan(POSTGRES_data)][0:1000]/divider


# plt.figure(figsize=(4, 3))
# # option 1, specify props dictionaries
# c = "red"
# plt.boxplot(data[:, :3], positions=[1, 2, 3], notch=True, patch_artist=True,
#             boxprops=dict(facecolor=c, color=c),
#             capprops=dict(color=c),
#             whiskerprops=dict(color=c),
#             flierprops=dict(color=c, markeredgecolor=c),
#             medianprops=dict(color=c),
#             )


# # option 2, set all colors individually
# c2 = "purple"
# box1 = plt.boxplot(data[:, ::-2]+1, positions=[1.5, 2.5,
#                                                3.5], notch=True, patch_artist=True)
# for item in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
#         plt.setp(box1[item], color=c2)
# plt.setp(box1["boxes"], facecolor="purple")
# plt.setp(box1["fliers"], markeredgecolor="purple")


# plt.xlim(0.5, 4)
# plt.xticks([1, 2, 3], [1, 2, 3])
# plt.show()



def save_to_plot():
	# agg backend is used to create plot as a .png file
	mpl.use('agg')
	# combine these different collections into a list
	data_to_plot = [BITCOIN_data, ETHEREUM_data, MULTICHAIN_data, STELLAR_data, EOS_data, IOTA_data, HYPERLEDGER_data, POSTGRES_data]
	# Create a figure instance
	fig = plt.figure(1, figsize=(9, 6))
	# Create an axes instance
	ax = fig.add_subplot(111)
	# Create the boxplot
	medianprops = dict(linewidth=1, color='black')

	bp = ax.boxplot(data_to_plot, patch_artist=True,
	           showfliers=False, medianprops=medianprops)
	## change outline color, fill color and linewidth of the boxes
	for box in bp['boxes']:
		# change outline color
		box.set(color='#A9A9A9', linewidth=2)
		# change fill color
		box.set(facecolor='#A9A9A9')
	# Show the median as a lable
	medians = [np.median(BITCOIN_data), np.median(
		ETHEREUM_data), np.median(MULTICHAIN_data), np.median(STELLAR_data), np.median(EOS_data), np.median(IOTA_data), np.median(HYPERLEDGER_data), np.median(POSTGRES_data)]
	median_labels = [str(np.around(s).astype(int)) for s in medians]
	pos = range(len(medians))
	for tick, label in zip(pos, ax.get_xticklabels()):
		ax.text(pos[tick]+1.3, medians[tick]-0.1, f"{median_labels[tick]} ms", va='bottom',
                    horizontalalignment='left', verticalalignment='center', size='x-small', color='black', weight='semibold')
	# Set labels etc.
	ax.set_xticklabels(['BITCOIN', 'ETHEREUM', 'MULTICHAIN', 'STELLAR', 'EOS', 'IOTA', 'HYPERLEDGER', 'POSTGRES'])
	ax.set_ylabel('Average time per transaction using 1000 samples (in seconds)')
	ax.set_yscale('log')
	ax.set_xlabel('Blockchain')
	ax.set_title('Performance Comparison')
	# Expand x axis a bit to the right, so there is space to label data
	ax.set_xlim(right=8.7)
	ax.yaxis.grid(True)
	
	# Save the figure and show
	plt.tight_layout()
	plt.style.use('seaborn-whitegrid')
	ax.grid(True)
	plt.savefig('performance_test/performance.pdf', format='pdf')

save_to_plot()
