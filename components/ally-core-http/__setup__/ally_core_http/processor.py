'''
Created on Nov 24, 2011

@package: ally core http
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the configurations for the processors used in handling the request.
'''

from ..ally_core.parsing_rendering import assemblyParsing
from ..ally_core.processor import invoking, default_charset, rendering, createDecoder, content, renderEncoder, \
    converterRequest, converterResponse, \
    blockIndexing
from ..ally_core.resources import injectorAssembly
from ..ally_http.processor import encoderPath, contentLengthDecode, \
    contentLengthEncode, methodOverride, allowEncode, contentTypeRequestDecode, \
    contentTypeResponseEncode, methodOverrideAllow
from ally.container import ioc
from ally.core.http.impl.processor.content_index import \
    ContentIndexEncodeHandler
from ally.core.http.impl.processor.explain_error import ExplainErrorHandler
from ally.core.http.impl.processor.headers.content_disposition import \
    ContentDispositionDecodeHandler
from ally.core.http.impl.processor.internal_error import \
    InternalDevelErrorHandler
from ally.core.http.impl.processor.method_invoker import MethodInvokerHandler
#TODO: from ally.core.http.impl.processor.parameter import ParameterHandler
from ally.core.http.impl.processor.parsing_multipart import \
    ParsingMultiPartHandler
from ally.core.http.impl.processor.path_encoder_invoker import InvokerPathEncoderHandler
#TODO: from ally.core.http.impl.processor.redirect import RedirectHandler
from ally.core.http.impl.processor.uri import URIHandler
from ally.core.http.spec.codes import CODE_TO_STATUS, CODE_TO_TEXT
from ally.design.processor.assembly import Assembly
from ally.design.processor.handler import Handler
from ally.http.impl.processor.header_parameter import HeaderParameterHandler
from ally.http.impl.processor.method_override import METHOD_OVERRIDE
from ally.http.impl.processor.status import StatusHandler
from ..ally_http.processor import acceptRequestDecode
from ally.core.http.impl.processor.scheme import SchemeHandler

# --------------------------------------------------------------------
# Creating the processors used in handling the request

@ioc.config
def allow_method_override():
    '''
    If true will allow the method override by using the header 'X-HTTP-Method-Override', the GET can be override with
    DELETE and the POST with PUT.
    '''
    return True

@ioc.config
def read_from_params():
    '''If true will push the parameters names defined in 'header_parameters' as headers.'''
    return True

@ioc.config
def header_parameters():
    '''
    The names of the parameters to be considered as actual headers, overriding any true header value for that name, to this
    list the custom headers will be appended automatically.
    '''
    return []

@ioc.config
def root_uri_resources():
    '''
    This will be used for adjusting the encoded URIs to have a root URI. The value needs to have one and only one '%s' marker
    where the partial URI will be injected.
    !Attention this configuration needs to be in concordance with 'server_pattern_resources' configuration
    '''
    return 'resources/%s'

# --------------------------------------------------------------------

@ioc.entity
def headersCustom() -> set:
    '''
    Provides the custom header names defined by processors.
    '''
    return set()

@ioc.entity
def parametersAsHeaders() -> list:
    parameters = set(header_parameters())
    parameters.update(headersCustom())
    parameters = sorted(parameters)
    return parameters

# --------------------------------------------------------------------
# Header decoders

@ioc.entity
def internalDevelError() -> Handler: return InternalDevelErrorHandler()

@ioc.entity
def headerParameter() -> Handler:
    b = HeaderParameterHandler()
    b.parameters = parametersAsHeaders()
    return b

@ioc.entity
def contentDispositionDecode() -> Handler: return ContentDispositionDecodeHandler()

@ioc.entity
def methodInvoker() -> Handler: return MethodInvokerHandler()

# --------------------------------------------------------------------
# Header encoders

@ioc.entity
def contentIndexEncode() -> Handler:
    b = ContentIndexEncodeHandler()
    b.assembly = assemblyBlocks()
    return b

# --------------------------------------------------------------------

@ioc.entity
def uri() -> Handler: return URIHandler()

@ioc.entity
def scheme() -> Handler: return SchemeHandler()

@ioc.entity
def encoderPathInvoker() -> Handler:
    b = InvokerPathEncoderHandler()
    b.resourcesRootURI = root_uri_resources()
    return b

@ioc.entity
def parameter() -> Handler: return ParameterHandler()

@ioc.entity
def parsingMultiPart() -> Handler:
    b = ParsingMultiPartHandler()
    b.charSetDefault = default_charset()
    b.parsingAssembly = assemblyParsing()
    b.populateAssembly = assemblyMultiPartPopulate()
    return b

@ioc.entity
def redirect() -> Handler:
    b = RedirectHandler()
    b.redirectAssembly = assemblyRedirect()
    return b

@ioc.entity
def statusCodeToStatus(): return dict(CODE_TO_STATUS)

@ioc.entity
def statusCodeToText(): return dict(CODE_TO_TEXT)

@ioc.entity
def status() -> Handler:
    b = StatusHandler()
    b.codeToStatus = statusCodeToStatus()
    b.codeToText = statusCodeToText()
    return b

@ioc.entity
def explainError(): return ExplainErrorHandler()

# --------------------------------------------------------------------

@ioc.entity
def assemblyResources() -> Assembly:
    '''
    The assembly containing the handlers that will be used in processing a REST request.
    '''
    return Assembly('REST resources')

@ioc.entity
def assemblyMultiPartPopulate() -> Assembly:
    '''
    The assembly containing the handlers that will populate data on the next request content.
    '''
    return Assembly('Multipart content')

@ioc.entity
def assemblyBlocks() -> Assembly:
    '''
    The assembly containing the indexing blocks providers.
    '''
    return Assembly('Blocks')

# --------------------------------------------------------------------

@ioc.before(headersCustom)
def updateHeadersCustom():
    if allow_method_override(): headersCustom().add(METHOD_OVERRIDE.name)

@ioc.before(assemblyResources)
def updateAssemblyResources():
    assemblyResources().add(internalDevelError(), injectorAssembly(), converterRequest(), uri(), methodInvoker(),
                            contentTypeRequestDecode(), contentLengthDecode(), acceptRequestDecode(), rendering(),
                            #parsingMultiPart(),
                            content(), scheme(), invoking(), converterResponse(), encoderPath(),
                            encoderPathInvoker(), renderEncoder(), status(), explainError(), contentIndexEncode(),
                            contentTypeResponseEncode(), contentLengthEncode(), allowEncode()
                            )
    

# TODO: Gabriel: add the folowing
#        redirect(),
#        
#        createDecoder(),
#        parameter(), 
    
    if allow_method_override():
        assemblyResources().add(methodOverride(), before=methodInvoker())
        assemblyResources().add(methodOverrideAllow(), after=methodInvoker())
    if read_from_params(): assemblyResources().add(headerParameter(), after=internalDevelError())

@ioc.before(assemblyMultiPartPopulate)
def updateAssemblyMultiPartPopulate():
    assemblyMultiPartPopulate().add(contentTypeRequestDecode(), contentDispositionDecode())
    
@ioc.before(assemblyBlocks)
def updateAssemblyBlocks():
    assemblyBlocks().add(blockIndexing())

