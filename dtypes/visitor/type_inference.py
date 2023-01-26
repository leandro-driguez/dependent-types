from .generic import GenericVisitor, visualizer
from dtypes.ranges import Range, RangeSet, RangeDict
from copy import deepcopy
from dtypes.ast import Attr, Constant, Eq, Ne, Lt, Gt, Le, Ge, Or, And
from sys import maxsize as oo

class TypeInference(GenericVisitor):

    def get(self, dtype, ctx = {}):
        return self.visit(dtype.contraint, ctx)

    # @visualizer(True)
    def visit(self, dtype, ctx={}):
        return super().visit(dtype, ctx)

    def visit_Gt(self, dtype, ctx = {}):

        if isinstance(dtype.left, Attr) and isinstance(dtype.right, Constant):
            ctx_copy = deepcopy(ctx)

            if dtype.left.attr not in ctx_copy['vars']:
                ctx_copy['vars'][dtype.left.attr] = f'var_{len(ctx_copy["vars"])}'

            var = ctx_copy['vars'][dtype.left.attr]
            ctx_copy['ranges'][var] = Range(dtype.right.value, oo, include_start=False)
            
            return ctx_copy

    def visit_Lt(self, dtype, ctx = {}):
        
        if isinstance(dtype.left, Attr) and isinstance(dtype.right, Constant):
            ctx_copy = deepcopy(ctx)
            
            if dtype.left.attr not in ctx_copy['vars']:
                ctx_copy['vars'][dtype.left.attr] = f'var_{len(ctx_copy["vars"])}'

            var = ctx_copy['vars'][dtype.left.attr]
            ctx_copy['ranges'][var] = Range(-oo, dtype.right.value, include_start=False)
            
            return ctx_copy

    def visit_Ge(self, dtype, ctx = {}):

        if isinstance(dtype.left, Attr) and isinstance(dtype.right, Constant):
            ctx_copy = deepcopy(ctx)

            if dtype.left.attr not in ctx_copy['vars']:
                ctx_copy['vars'][dtype.left.attr] = f'var_{len(ctx_copy["vars"])}'

            var = ctx_copy['vars'][dtype.left.attr]
            ctx_copy['ranges'][var] = Range(dtype.right.value, oo)
            
            return ctx_copy

    def visit_Le(self, dtype, ctx = {}):
        
        if isinstance(dtype.left, Attr) and isinstance(dtype.right, Constant):
            ctx_copy = deepcopy(ctx)

            if dtype.left.attr not in ctx_copy['vars']:
                ctx_copy['vars'][dtype.left.attr] = f'var_{len(ctx_copy["vars"])}'

            var = ctx_copy['vars'][dtype.left.attr]
            ctx_copy['ranges'][var] = Range(-oo, dtype.right.value, include_start=False, include_end=True)
            
            return ctx_copy

    def visit_Eq(self, dtype, ctx = {}):
        
        if isinstance(dtype.left, Attr) and isinstance(dtype.right, Constant):
            ctx_copy = deepcopy(ctx)

            if dtype.left.attr not in ctx_copy['vars']:
                ctx_copy['vars'][dtype.left.attr] = f'var_{len(ctx_copy["vars"])}'

            var = ctx_copy['vars'][dtype.left.attr]
            ctx_copy['ranges'][var] = Range(dtype.right.value, dtype.right.value, include_end=True)
            
            return ctx_copy

    def visit_Ne(self, dtype, ctx = {}):
        
        if isinstance(dtype.left, Attr) and isinstance(dtype.right, Constant):

            ctx_copy = deepcopy(ctx)
            if dtype.left.attr not in ctx_copy['vars']:
                ctx_copy['vars'][dtype.left.attr] = f'var_{len(ctx_copy["vars"])}'

            var = ctx_copy['vars'][dtype.left.attr]
            ctx_copy['ranges'][var] = RangeSet(f"({-oo},{dtype.right.value})",f"({dtype.right.value},{oo})")

            return ctx_copy    

    def visit_Or(self, dtype, ctx = {}):
        
        if isinstance(dtype.left, (Attr, Eq, Ne, Lt, Gt, Le, Ge, Or, And)) \
        and isinstance(dtype.right, (Attr, Eq, Ne, Lt, Gt, Le, Ge, Or, And)):
            ctx_copy  = deepcopy(ctx)
            
            ctx_left = self.visit(dtype.left, ctx_copy)
            ctx_right = self.visit(dtype.right, ctx_copy)
            # print(f'\n\n1 { ctx_left }\n  { ctx_right }\n\n')
            
            ctx_left['ranges']  = RangeDict(ctx_left['ranges'])
            # print(f'bye! {ctx_right["ranges"]}')
            ctx_right['ranges'] = RangeDict(ctx_right['ranges'])
            ctx_copy['ranges'] = ctx_left['ranges'] | ctx_right['ranges']

            # print(f'\n\n2 { ctx_copy }\n\n')

            return ctx_copy

    def visit_And(self, dtype, ctx = {}):
        
        if isinstance(dtype.left, (Attr, Eq, Ne, Lt, Gt, Le, Ge)) \
        and isinstance(dtype.right, (Attr, Eq, Ne, Lt, Gt, Le, Ge)):
            ctx_copy  = deepcopy(ctx)
            
            ctx_left  = self.visit(dtype.left, ctx_copy)
            ctx_right = self.visit(dtype.right, ctx_copy)
            
            ctx_left['ranges']  = RangeDict(ctx_left['ranges'])
            ctx_right['ranges'] = RangeDict(ctx_right['ranges'])

            ctx_copy['ranges'] = ctx_left['ranges'] & ctx_right['ranges']

            return ctx_copy

    # def visit_Mul(self, dtype, ctx = {}):
    #     ...

    # def visit_Ne(self, dtype, ctx = {}):
    #     ...
