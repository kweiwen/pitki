"""
Communicates with a 32-bit .NET library via the :class:`~.dotnet32.DotNet32` class.

Example of a module that can be executed within a 64-bit Python interpreter which can
communicate with a 32-bit .NET library, :ref:`dotnet_lib32.dll <dotnet-lib>` that is
hosted by a 32-bit Python server, :mod:`.dotnet32`. A 64-bit process cannot load a
32-bit library and therefore `inter-process communication <ipc_>`_ is used to
interact with a 32-bit library from a 64-bit process.

:class:`~.dotnet64.DotNet64` is the 64-bit client and :class:`~.dotnet32.DotNet32`
is the 32-bit server for `inter-process communication <ipc_>`_.

.. _ipc: https://en.wikipedia.org/wiki/Inter-process_communication
"""
import os

from msl.loadlib import Client64


class DotNet64(Client64):
    """Communicates with the 32-bit C# :ref:`dotnet_lib32.dll <dotnet-lib>` library.

    This class demonstrates how to communicate with a 32-bit .NET library if an instance of this
    class is created within a 64-bit Python interpreter.
    """
    def __init__(self):
        # specify the name of the corresponding 32-bit server module, dotnet32, which hosts
        # the 32-bit .NET library -- dotnet_lib32.dll.
        super(DotNet64, self).__init__(module32='dotnet32', append_sys_path=os.path.dirname(__file__))
        print(os.path.dirname(__file__))

    def get_class_names(self):
        """Return the class names in the library.

        See the corresponding 32-bit :meth:`~.dotnet32.DotNet32.get_class_names` method.

        Returns
        -------
        :class:`list` of :class:`str`
            The names of the classes that are available in :ref:`dotnet_lib32.dll <dotnet-lib>`.        
        """
        return self.request32('get_class_names')