import numpy as np
import openmdao.api as om
from openmdao.api import Problem, IndepVarComp, ScipyOptimizeDriver
from openaerostruct.geometry.utils import generate_mesh
from openaerostruct.geometry.geometry_group import Geometry
from openaerostruct.aerodynamics.aero_groups import AeroPoint

from structures_group import StructuresGroup
from thrust_group import TurbofanGroup
from weightGroup import weightGroup
from cost_group import CostGroup

prob = Problem()

comp = IndepVarComp()
#comp.add_output('v', val=248.136, units='m/s')
#comp.add_output('alpha', val=5., units='deg')
#comp.add_output('Mach_number', val=0.84)
#comp.add_output('re', val=1.e6, units='1/m')
#comp.add_output('rho', val=0.38, units='kg/m**3')
#comp.add_output('cg', val=np.zeros((3)), units='m')


comp.add_output('wing_span',val=44, units='m')
comp.add_output('chord',val=0.1, units='m')

comp.add_output('altitude_km', val=4400,units='m')
comp.add_output('drag', val=34400, units='kN')
#comp.add_output('sealevel_thrust', val=74400)
comp.add_output('velocity_ms', val=248.136,units='m/s')

#comp.add_input('gross_weight',val=187346)
comp.add_output('wing_area',val=17346,units='m**2')
comp.add_output('horizontal_tail_area',val=17346, units='m')
comp.add_output('bw',val=17346)

comp.add_output('We', val=187346, units='kg')
comp.add_output('Wfr', val=34300, units='kg')

prob.model.add_subsystem('inputs_comp', comp, promotes=['*'])

comp = IndepVarComp()
comp.add_output('payload_weight',val=4400, units='kg')
comp.add_output('crew_weight',val=4400, units='kg')
comp.add_output('empty_weight_fraction',val=0.4)
comp.add_output('fuel_weight_fraction', val=0.5)

comp.add_output('A', val=8.) ## still need to fix these values #Modeling Constants
comp.add_output('B', val=0.2)#Modeling Constants
comp.add_output('n', val=8.)#Modeling Constants
comp.add_output('k', val=0.2) #Modeling Constants

comp.add_output('MHFH', val=10) ## Maintaince Hour Per Flight Hour
comp.add_output('M_max', val=0.83) ## Engine max mach number
comp.add_output('T_max', val=74400, units='kN') ## Engine max Thrust
comp.add_output('EN', val=500 * 2) ## Engine Number
comp.add_output('FH', val=3500, units='h') ###flight hour
comp.add_output('FTA', val=3) ###FTA flight test
comp.add_output('Q', val=500) ### Less number production
comp.add_output('Tinlet', val = 3303, units='K') ## Turbine inlet temperature

prob.model.add_subsystem('constants', comp, promotes=['*'])

#geom_group = Geometry(surface=surface)
#prob.model.add_subsystem(surface['name'], geom_group)

# Create the aero point group, which contains the actual aerodynamic
# analyses
#aero_group = AeroPoint(surfaces=[surface])
#point_name = 'aero_point_0'
#prob.model.add_subsystem(point_name, aero_group,
#    promotes_inputs=['v', 'alpha', 'Mach_number', 're', 'rho', 'cg'])
#name = surface['name']
# Connect the mesh from the geometry component to the analysis point
#prob.model.connect(name + '.mesh', point_name + '.' + name + '.def_mesh')
# Perform the connections with the modified names within the
# 'aero_states' group.
#prob.model.connect(name + '.mesh', point_name + '.aero_states.' + name + '_def_mesh')
#prob.model.connect(name + '.t_over_c', point_name + '.' + name + '_perf.' + 't_over_c')




group = StructuresGroup()
prob.model.add_subsystem('structure_group', group, promotes=['*'])
group = TurbofanGroup()
prob.model.add_subsystem('propulsion_group', group, promotes=['*'])
group = weightGroup()
prob.model.add_subsystem('weight_group', group, promotes=['*'])
group = CostGroup()
prob.model.add_subsystem('cost_group', group, promotes=['*'])

#prob.driver = ScipyOptimizeDriver()
#prob.driver.options['optimizer'] = 'SLSQP'
#prob.driver.options['tol'] = 1e-15
#prob.driver.options['disp'] = True

prob.setup()
prob.run_model()
#prob.run_driver()

prob.check_partials(compact_print=True)