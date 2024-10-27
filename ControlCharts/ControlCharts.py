import numpy as np

class ControlCharts:
    def __init__(self, arr: list, ucl:bool = None, lcl:bool = None, target: bool = None, stages: bool = None):
        self.arr:list = np.array(arr)
        self.mean:float = np.mean(self.arr)
        self.target:float = target
        self.stages:list = np.array(stages)
        self.standard_deviation:float = self.get_moving_standard_deviation()
        self.list_fail = np.zeros(len(self.arr), dtype=int)
        
        if ucl:
            self.ucl:float = ucl

        else:
            self.ucl:float = self.mean + (3 * self.standard_deviation)

        if lcl:
            self.lcl:float = lcl

        else:
            self.lcl:float = self.mean - (3 * self.standard_deviation)

        self.test_1()
        self.test_2()
        self.test_3()
        self.test_5()

    def get_moving_standard_deviation(self) -> list:
        differences = np.abs(np.diff(self.arr))
        return np.mean(differences) / 1.128

    def test_1(self) -> None:
        """
            One point more than 3 standard deviation from the center line
        """
        for i in range(len(self.arr)):
            if self.arr[i] > self.ucl or self.arr[i] < self.lcl:
                self.list_fail[i] = 1
            
    def test_2(self) -> None:  
        """
            9 points in a row is on the same side of the center line (mean)
        """
        for i in range(len(self.arr) - 9):
            if all(self.arr[j] < self.mean for j in range(i, i+9)):
                self.list_fail[i + 8] = 2

            elif all(self.arr[j] > self.mean for j in range(i, i+9)):
                self.list_fail[i + 8] = 2
        
    def test_3(self) -> None:
        """
            Six points in a row, all increasing or all decreasing
        """
        for i in range(len(self.arr) - 6):
            if all(self.arr[j] > self.arr[j+1] for j in range(i, i + 6)):
                self.list_fail[i+5] = 3
            elif all(self.arr[j] < self.arr[j+1] for j in range(i, i + 6)):
                self.list_fail[i+5] = 3

    def test_4(self) -> None:
        """
            Fourteen points in a row is alternating up and down
        """

    # TODO: needs to be refined
    def test_5(self) -> None:
        """
            Two out of three points are more than 2 sigma from the center line
        """
        two_sigma:float = 2 * self.standard_deviation
        failed_data_points:int = np.zeros(len(self.arr), dtype=int)

        for i in range(len(self.arr) - 3):
            if any(self.arr[j] > self.mean + two_sigma for j in range(i, i+3)):
                failed_data_points[i] = i

            if any(self.arr[j] < self.mean - two_sigma for j in range(i, i+3)):
                failed_data_points[i] = i
        
    def test_6(self) -> None:
        pass

    def test_7(self) -> None:
        pass

    def test_8(self) -> None:
        pass

    def print_chart(self) -> None:
        pass

    def return_dataframe_with_failed_tests(self) -> None:
        pass