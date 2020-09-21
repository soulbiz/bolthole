# bolthole Orchestrated gRPC chat
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from dotenv import load_dotenv
import os
import sys

from bolthole.app import serve

if __name__ == "__main__":
    load_dotenv()

    service_address = os.getenv('SERVICE_ADDRESS')
    if not service_address:
        print("missing environment variable SERVICE_ADDRESS")
        sys.exit(1)

    print("starting grpc server")
    serve(service_address)
