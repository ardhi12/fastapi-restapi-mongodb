"""
Karena JSONResponse pada controller tidak dapat menerima respon dalam bentuk object (JSON Error Serializable),
maka transformer ini adalah cara untuk memformat dari Object menjadi JSON. 
hasil dari transform ini digunakan sebagai isi pada bagian "data"/"values" pada response dari endpoint
"""

def transform(items):
    array = []

    for item in items:
        array.append(singleTransform(item))
    return array


def singleTransform(values):
    return {
        "id": str(values.id),
        "name": values.name,
    }
