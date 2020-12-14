import sys
sys.path.insert(0, "..")
import logging
import time
import warnings


try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()

from opcua import ua
from opcua import Client
from opcua import Node


class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another 
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


def cancella_contenuto_array_caratteri(client, ns, i, ARRAY_DIM):
    """
    resetta il contenuto di un array di char all'interno della DB di scambio
    :param client: oggetto per la connessione OPC UA
    :param ns: namespace id
    :param i:  indice del namespace
    :param ARRAY_DIM: dimensioni del vettore definito nella DB di scambio
    :return:
    """
    for pos in range(ARRAY_DIM+1):
        stringa = "" + "ns="+str(ns)+";i="+str(i+pos+1)
        var = client.get_node(stringa)
        datavalue = ua.DataValue(ua.Variant(ord(" "), ua.VariantType.Byte))
        var.set_data_value(datavalue)


def scrivi_stringa(client, ns, i, STR_VAL, ARRAY_DIM):
    """
    scrive la stringa all'interno dell'array di caratteri del DB
    :param client: oggetto per la connessione OPC UA
    :param ns: namespace id
    :param i:  indice del namespace
    :param STR_VAL: stringa da scrivere
    :param ARRAY_DIM: dimensioni del vettore definito nella DB di scambio
    :return:
    """

    for pos, char in enumerate(STR_VAL):
        if pos < ARRAY_DIM+1:
            stringa = "" + "ns="+str(ns)+";i="+str(i+pos+1)
            var = client.get_node(stringa)
            datavalue = ua.DataValue(ua.Variant(ord(char), ua.VariantType.Byte))
            var.set_data_value(datavalue)
        else:
            warnings.warn("attenzione limite vettore oltrepassato : la stringa e' stata troncata")
            return


def leggi_vettore_caratteri(client, ns, i, ARRAY_DIM):
    """
    Legge il contenuto di un array di char all'interno della DB di scambio
    :param client: oggetto per la connessione OPC UA
    :param ns: namespace id
    :param i:  indice del namespace
    :param ARRAY_DIM: dimensioni del vettore definito nella DB di scambio
    :return: stringa letta nel DB
    """
    out = ""
    for pos in range(ARRAY_DIM+1):
        stringa = "" + "ns="+str(ns)+";i="+str(i+pos+1)
        var = client.get_node(stringa)
        var.get_data_value()  # get value of node as a DataValue object
        VAL = var.get_value()  # get value of node as a python builtin
        out += chr(VAL)
    return out

def scrivi_float(client, ns, i, VAL):
    """
    scrive un valore float all'interno di una variabile
    :param client: oggetto per la connessione OPC UA
    :param ns: namespace id
    :param i:  indice del namespace
    :param VAL: valore da scrivere
    :return:
    """
    stringa = "" + "ns="+str(ns)+";i="+str(i)
    var = client.get_node(stringa)
    # print(var)
    datavalue = ua.DataValue(ua.Variant(VAL, ua.VariantType.Float))
    var.set_data_value(datavalue)

def leggi_valore(client, ns, i):
    """
    legge il valore di una variabile
    :param client: oggetto per la connessione OPC UA
    :param ns: namespace id
    :param i:  indice del namespace
    :return:
    """
    stringa = "" + "ns="+str(ns)+";i="+str(i)
    var = client.get_node(stringa)
    # print(var)
    var.get_data_value()  # get value of node as a DataValue object
    VAL = var.get_value()  # get value of node as a python builtin
    return VAL


def connect_to_plc(indirizzo):
    client = Client(indirizzo)
    return client



def main():
    logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("KeepAlive")
    #logger.setLevel(logging.DEBUG)

    client = connect_to_plc("opc.tcp://192.168.0.1:4840")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    try:
        client.connect()
        client.load_type_definitions()  # load definition of server specific structures/extension objects

        val_var = leggi_valore(client,4,35)
        print("valore contatore :", val_var)

        # scrivi_float(client,4,30,45)

        # nodo ed id della posizione iniziale della stringa che si vuole scrivere
        ns = 4
        id_s = 14 

        cancella_contenuto_array_caratteri(client,ns,id_s,10)

        scrivi_stringa(client,ns,id_s,"prova_scrittura_array", 10)

        array_letto = leggi_vettore_caratteri(client,ns,id_s,10)
        print("array letto :",array_letto)
        # embed()
    finally:
        client.disconnect()



if __name__ == "__main__":
    main()