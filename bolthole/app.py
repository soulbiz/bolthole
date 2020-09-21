# bolthole Orchestrated gRPC chat
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from concurrent import futures
import grpc

import bolthole_pb2_grpc
from bolthole.chat import ChatServicer

# Define max number of workers
__MAX_THREAD_POOL_EXECUTOR_WORKERS__ = 10


def serve(address):
    """Serves the grpc server

    Parameters
    ----------
    address : str
        Server address interface:host
    """
    server = grpc.server(futures.ThreadPoolExecutor(
            max_workers=__MAX_THREAD_POOL_EXECUTOR_WORKERS__
        )
    )

    bolthole_pb2_grpc.add_ChatServicer_to_server(ChatServicer(), server)

    # TODO: secure port TLS
    server.add_insecure_port(address)

    server.start()
    server.wait_for_termination()
