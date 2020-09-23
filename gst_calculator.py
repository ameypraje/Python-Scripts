"""
UTILITY TO GET GST VALUES
While initialize class provide any two parameter to calculate other two.
  For eg.
    gst = GST(gst_percent=10, gross_amount=1100, net_amount=1000, gst_amount=100)
    
    where, 
      gst_percent is tax percent applied/to be applied
      gross_amount is price inclusive of tax
      net_amount is price exclusive of tax
      gst_amount is tax value.

"""


class InCompleteDataError(Exception):
    pass


class GST:

    """
        This class is to calculate GST amount for india.

    """


    def __init__(self, gst_percent=None, gross_amount=None, net_amount=None, gst_amount=None):
        self.gst_percent = gst_percent
        self.gst_amount = gst_amount
        self.gross_amount = gross_amount
        self.net_amount = net_amount
    
        self.calculate_gst()

    def get_gst_percent(self):
        """
            Returns gst percentage
        """
        return self.gst_percent

    def get_gst_amount(self):
        """
            Returns gst amount
        """
        return self.gst_amount

    def get_net_amount(self):
        """
            Returns net amount i.e. exclusive of tax
        """
        return self.net_amount

    def get_gross_amount(self):
        """
            Returns gross amount i.e. inclusive of tax
        """
        return self.gross_amount
    
    def calculate_gst_percent(self):
        """
            Calculate gst percent based on GROSS AMOUNT & NET AMOUNT
        """
        self.gst_percent = ((self.gross_amount - self.net_amount) * 100) / self.net_amount

    def calculate_gst_amount(self):
        """
            Calculate gst amount based on GROSS AMOUNT & NET AMOUNT
        """
        self.gst_amount = self.gross_amount - self.net_amount

    def calculate_gst_amount_by_gross_amount(self):
        """
            Calculate gst amount based on GROSS AMOUNT & GST PERCENT
        """
        self.gst_amount = self.gross_amount - (self.gross_amount * (100 / (100 + self.gst_percent)))

    def calculate_gst_amount_by_net_amount(self):
        """
            Calculate gst amount based on GST PERCENT & NET AMOUNT
        """
        self.gst_amount = (self.net_amount * self.gst_percent) / 100

    def calculate_net_amount_by_gst_amount(self):
        """
            Calculate net amount based on GROSS AMOUNT & GST AMOUNT
        """
        self.net_amount = self.gross_amount - self.gst_amount

    def calculate_net_amount_by_gst_amount_and_gst_percent(self):
        """
            Calculate net amount based on gst amount and gst percent
        """
        self.net_amount = (self.gst_amount * 100) / self.gst_percent

    def calculate_gross_amount_by_gst_amount(self):
        """
            Calculate gross amount based on GST AMOUNT & NET AMOUNT
        """
        self.gross_amount = self.net_amount + self.gst_amount

    def calculate_gst(self):
        """
            Calculate all fields based on available inputs
            Raises error of input is incomplete
        """

        if all([self.gross_amount, self.net_amount]):
            self.calculate_gst_amount()
            self.calculate_gst_percent()
        
        elif any([self.gross_amount, self.net_amount]):

            if self.gst_percent:
                if self.gross_amount:
                    self.calculate_gst_amount_by_gross_amount()
                    self.calculate_net_amount_by_gst_amount()
                else:
                    self.calculate_gst_amount_by_net_amount()
                    self.calculate_gross_amount_by_gst_amount()

            elif self.gst_amount:
                if self.gross_amount:
                    self.calculate_net_amount_by_gst_amount()
                else:
                    self.calculate_gross_amount_by_gst_amount()

                self.calculate_gst_percent()

            else:
                raise InCompleteDataError("Atleast two parameters required")
        
        elif all([self.gst_percent, self.gst_amount]):
            self.calculate_net_amount_by_gst_amount_and_gst_percent()
            self.calculate_gross_amount_by_gst_amount()

        else:
            raise InCompleteDataError("Atleast two parameters required")
