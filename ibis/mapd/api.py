import ibis.common as com
from ibis.config import options
from ibis.mapd.client import EXECUTION_TYPE_CURSOR, MapDClient
from ibis.mapd.compiler import compiles, dialect, rewrites  # noqa: F401


def compile(expr, params=None):
    """
    Force compilation of expression as though it were an expression depending
    on MapD. Note you can also call expr.compile()

    Returns
    -------
    compiled : string
    """
    from ibis.mapd.compiler import to_sql

    return to_sql(expr, dialect.make_context(params=params))


def verify(expr, params=None):
    """
    Determine if expression can be successfully translated to execute on
    MapD
    """
    try:
        compile(expr, params=params)
        return True
    except com.TranslationError:
        return False


def connect(
    uri=None,
    user=None,
    password=None,
    host=None,
    port=None,
    database=None,
    protocol=None,
    sessionid=None,
    execution_type=EXECUTION_TYPE_CURSOR,
    ospyconn=None,
):
    """Create a MapDClient for use with Ibis

    Parameters could be

    :param uri: str
    :param user: str
    :param password: str
    :param host: str
    :param port: int
    :param database: str
    :param protocol: str
    :param execution_type: int
    :param ospyconn: pymapd.connection.Connection

    Examples
    --------
    You can either pass the same parameters that pymapd accepts,
    or an existing pymapd conneciton object. In both cases the
    execution type can also be passed.

    >>> connect('mapd://mapd:HyperInteractive@localhost:6274/mapd?'
    ...         'protocol=binary', execution_type=1)
    >>> connect(user='mapd', password='HyperInteractive', host='localhost',
    ...         port=6274, dbname='mapd')
    >>> connect(sessionid='XihlkjhdasfsadSDoasdllMweieisdpo', host='localhost',
    ...         port=6273, protocol='http', execution_type=3)
    >>> connect(ospyconn=omnisciconn, execution_type=2)

    Returns
    -------
    MapDClient

    """
    client = MapDClient(
        uri=uri,
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
        protocol=protocol,
        sessionid=sessionid,
        execution_type=execution_type,
        ospyconn=ospyconn,
    )

    if options.default_backend is None:
        options.default_backend = client

    return client
