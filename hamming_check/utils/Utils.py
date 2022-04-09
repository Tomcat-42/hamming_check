class Utils(object):

    @staticmethod
    def is_power_of_two(x) -> bool:
        return x > 0 and (not (x & (x - 1)))
