"""
A wrapper around a 32-bit .NET library, :ref:`dotnet_lib32 <dotnet-lib>`.

Example of a server that loads a 32-bit .NET library, :ref:`dotnet_lib32.dll <dotnet-lib>`
in a 32-bit Python interpreter to host the library. The corresponding :mod:`~.dotnet64`
module can be executed by a 64-bit Python interpreter and the :class:`~.dotnet64.DotNet64`
class can send a request to the :class:`~.dotnet32.DotNet32` class which calls the
32-bit library to execute the request and then return the response from the library.
"""
import os

from msl.loadlib import Server32

class DotNet32(Server32):

    def __init__(self, host, port, **kwargs):
        """
        Example of a class that is a wrapper around a 32-bit .NET Framework library,
        :ref:`dotnet_lib32.dll <dotnet-lib>`. `Python for .NET <https://pythonnet.github.io/>`_
        can handle many native Python data types as input arguments.

        Parameters
        ----------
        host : :class:`str`
            The IP address of the server.
        port : :class:`int`
            The port to open on the server.

        Note
        ----
        Any class that is a subclass of :class:`~msl.loadlib.server32.Server32` **MUST**
        provide two arguments in its constructor: `host` and `port` (in that order)
        and `**kwargs`. Otherwise the ``server32`` executable, see
        :class:`~msl.loadlib.start_server32`, cannot create an instance of the
        :class:`~msl.loadlib.server32.Server32` subclass.
        """
#         super(DotNet32, self).__init__('QACTLib.dll', 'net', host, port)
        super(DotNet32, self).__init__('dotnet_lib32.dll', 'net', host, port)
        
        print(os.path.dirname(__file__))

    def get_class_names(self):
        """Returns the class names in the library.

        See the corresponding 64-bit :meth:`~.dotnet64.DotNet64.get_class_names` method.

        Returns
        -------
        :class:`list` of :class:`str`
            The names of the classes that are available in :ref:`dotnet_lib32.dll <dotnet-lib>`.
        """
        return ';'.join(str(name) for name in self.assembly.GetTypes()).split(';')
