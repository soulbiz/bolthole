# bolthole Orchestrated gRPC chat
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from google.protobuf.empty_pb2 import Empty
import queue
import time

import bolthole_pb2
import bolthole_pb2_grpc
from bolthole.message import Message
from bolthole.user import User

# Define max queue size (zero or less is infinite)
__MAX_QUEUE_SIZE__ = 0


class ChatServicer(bolthole_pb2_grpc.ChatServicer):
    """Class to handle the Chat service implementation

    Attributes
    ----------
    __queues__ : list with users chat history queues
    __users__ : dictionary with users

    Methods
    -------
    __init__(self) : Constructor
    GetMessage(self, request, context) : Handles the GetMessage
    """

    def __init__(self):
        """Constructor
        """
        # Initialize queues
        self.__queues__ = []
        self.__users__ = {}

    def GetMessage(self, request, context):
        """Handles the GetMessage

        Parameters
        ----------
        request : Grpc request
            Client request
        context : Context
            Connection context
        """
        if not request.user.id:
            context.set_details('bad argument user id')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return None
        if not request.user.name:
            context.set_details('bad argument user name')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return None

        if self.__users__.get(request.user.id):
            context.set_details('user id already in use')
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return None

        # TODO: handle active flag

        user = User(request.user.id, request.user.name)
        self.__users__[request.user.id] = user
        messages = queue.Queue(maxsize=__MAX_QUEUE_SIZE__)
        self.__queues__.append(messages)
        print("connected new user '%s'" % request.user.id)

        while context.is_active():
            # TODO: timeout(?)
            message = messages.get()
            yield bolthole_pb2.Message(
                id=message.user.id,
                content=message.content,
            )

        print("client disconnected")
        del self.__users__[request.user.id]
        self.__queues__.remove(messages)

        return None

    def SendMessage(self, request, context):
        """Handles the SendMessage

        Parameters
        ----------
        request : Grpc request
            Client request
        context : Context
            Connection context
        """
        if not request.id:
            context.set_details('bad argument id')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return None
        if not request.content:
            context.set_details('bad argument content')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return None

        user = self.__users__.get(request.id)
        if not user:
            context.set_details('unknown user')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return None

        # TODO: handle timestamp

        message = Message(user, request.content)

        for queue in self.__queues__:
            queue.put(message)

        return Empty()
