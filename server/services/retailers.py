"""
Handle all actions on the retailer resource and is responsible for making sure
the calls get routed to the ERP service appropriately. As much as possible,
the interface layer should have no knowledge of the properties of the retailer
object and should just call into the service layer to act upon a retailer resource.
"""


###########################
#         Utilities       #
###########################


def retailer_to_dict(retailer):
    """
    Convert an instance of the Retailer model to a dict.

    :param retailer:  An instance of the Retailer model.
    :return:      A dict representing the retailer.
    """
    return {
        'id': retailer.get('id'),
        'contact': retailer.get('contact'),
        'address': retailer.get('address')
    }