#!/usr/bin/env python3
import numpy as np

import cloning_tools
import generic_tools
import gsheetclient

from datetime import datetime
from multiprocessing import Pool
import multiprocessing as multi

if __name__ == '__main__':

    now_start = str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    print("開始時刻は%s" %now_start)

    login_driver = cloning_tools.make_driver()
    product_list = cloning_tools.make_product_list(login_driver)
    product_details = cloning_tools.make_price(login_driver,product_list)

    all_data = np.concatenate([product_list, product_details])
    all_data_arr = all_data.tolist()
    print(all_data_arr)
    now = str(datetime.now().strftime("%Y.%m.%d  %H-%M-%S"))

    gsheetclient.GoogleSheets(all_data_arr).fillin()

    # generic_tools.writeDoodProductsOnGS(all_data,now)
    # generic_tools.analysing_data()

    now_finish = str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    print("終了時刻は%s" %now_finish)

    login_driver.quit()
