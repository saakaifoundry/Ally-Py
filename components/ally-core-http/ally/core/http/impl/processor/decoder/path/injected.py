'''
Created on Jul 30, 2013

@package: ally core http
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the model properties that are injected from the path.
'''

from ally.api.operator.type import TypeProperty
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor

# --------------------------------------------------------------------

class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Required
    path = requires(list)

class Element(Context):
    '''
    The element context.
    '''
    # ---------------------------------------------------------------- Required
    node = requires(Context)
    property = requires(TypeProperty)
    isInjected = requires(bool)
    
class Create(Context):
    '''
    The create context.
    '''
    # ---------------------------------------------------------------- Defined
    pathInjected = defines(dict, doc='''
    @rtype: dictionary{Context: Context}
    The decodings that are injected into the model from the path indexed by the node.
    ''')
    
class Decoding(Context):
    '''
    The decoding context.
    '''
    # ---------------------------------------------------------------- Required
    property = requires(TypeProperty)
    
# --------------------------------------------------------------------

@injected
class InjectedPathDecode(HandlerProcessor):
    '''
    Implementation for a handler that provides the model properties that are injected from the path.
    '''
    
    def __init__(self):
        super().__init__(Element=Element)
        
    def process(self, chain, create:Create, decoding:Decoding, invoker:Invoker, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Register the injected path decodings.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(create, Create), 'Invalid create %s' % create
        assert isinstance(decoding, Decoding), 'Invalid decoding %s' % decoding
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        
        if not decoding.property: return
        if not invoker.path: return
        
        for el in invoker.path:
            assert isinstance(el, Element), 'Invalid path element %s' % el
            if el.node and el.isInjected and el.property == decoding.property:
                if create.pathInjected is None: create.pathInjected = {}
                create.pathInjected[el.node] = decoding
                chain.cancel()  # Cancel the decode creation
                break
