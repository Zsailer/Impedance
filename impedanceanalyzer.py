# Find the machine and define it. 
from pyvisa.vpp43 import visa_library
visa_library.load_library(r"C:\Windows\System32\visa32.dll")
import visa
instr = visa.instrument("GPIB3::17::INSTR")

import os
import time
from IPython.core.display import Javascript

def UI():
    """This is a Javascript UI dynamically created by JQuery for the
    HP4192A impedance analyzer. You must have an html <div> with the
    ID = 'UI' to make this work. (i.e. <div id='UI'></div>)
    
    This will load all the buttons and switches necessary to run the
    machine. Notice that all the functions for a switch and select
    box are defined, so anyone can add more of these elements to the
    div as they please.
    
    The values are sent via the IPython messaging through the IPython
    kernel and are assigned to Python variables.
    
    The 'settings' dictionary maps the UI variable to the messaging
    protocol for the impedance analyzer.
    """
    
    return Javascript("""

    /*
    This Code uses JQuery in an IPython notebook to create a UI for the HP 4192A LF
    impedance analyzer. 

    Created by: Zach Sailer

    */

    function switch_box(name, variable) {
        return $('<div>').attr('align','right').addClass('span3').text(name+': ')
                .append($('<select/>').addClass('span3 switch-box').addClass(variable)
                .append(($('<option>').val('panel["'+ variable + '"]="On"').text('ON')))
                .append(($('<option>').val('panel["'+ variable + '"]="Off"').text('OFF'))));
    }

    function select_box(name, item, variable, len) {
        var box = $('<div>').attr('align','right').addClass('span3').text(name+': ').addClass(item+'div')
        var select = $('<select>').addClass('span3 select-box').addClass(item)
        for (var i=0;i<len;i++) {
            select = select.append($('<option>')
            .val('panel["'+ item + '"]="'+variable[i]+'"').text(variable[i]))
        };
        return box.append(select);
    };

    function osc_level() {
        var form = $('<form>').addClass('span3').attr('align', 'left')
        var field = $('<fieldset>')
                    .append('<label>Oscillation Level (Volts):</label>')
                    .append('<input class="osc_level">').attr('type','text')
        return form.append(field)
    };

    function reg_sweep(item, settings) {
        var form = $('<form>').addClass('span4')
        var field = $('<fieldset>')
                    .append('<legend>'+item+' Sweep</legend>')
                    .append('<label>Start '+item+'</label>')
                    .append('<input class="start_'+item+'">').attr('type','text')
                    .append('<label>Stop '+item+'</label>')
                    .append('<input class="stop_'+item+'">').attr('type','text')
                    .append('<label>Step '+item+'</label>')
                    .append('<input class="step_'+item+'">').attr('type','text')
        return $('<div>').addClass('sweep_div').append(form.append(field)).append(run_button(settings, true, item))
    };

    function sweep_select(settings) {
        return $('<div>').attr('align','right').addClass('span3').text('Type of Sweep:')
                .append($('<select/>').addClass('span3 switch-box').addClass('sweep_type')
                    .append(($('<option>').val('noFreq').text('No Sweep')))
                    .append(($('<option>').val('regFreq').text('Regular Frequency Sweep')))
                    .append(($('<option>').val('logFreq').text('Log Frequency Sweep')))
                    .append(($('<option>').val('regVolt').text('Voltage Bias Sweep')))
                    .append(($('<option>').val('custsweep').text('Custom Sweep')))
                    .change(function(){
                        var sel = $('.sweep_type').val();
                        if (sel == 'regFreq') {
                            $('.sweep_div').replaceWith(reg_sweep('Frequency', settings));
                        }
                        else if (sel == 'noFreq') {
                            $('.sweep_div').replaceWith(no_sweep(settings));
                        }
                        else if (sel == 'regVolt') {
                            $('.sweep_div').replaceWith(reg_sweep('Voltage',settings));
                        }
                        else if (sel == 'logFreq') {
                            $('.sweep_div').replaceWith(log_sweep(settings));
                        }
                        else if (sel == 'custsweep') {
                            $('.sweep_div').replaceWith($('<div>').addClass('sweep_div').append(run_button(settings, null, null)));
                        }
                    })
                );
    };

    function no_sweep(settings) {
        return $('<div>').attr('align','right').addClass('sweep_div span3').text('Type of test measurement:')
                .append($('<select/>').addClass('span3 switch-box').addClass('test_type')
                    .append(($('<option>').val('freq').text('Frequency')))
                    .append(($('<option>').val('volt').text('Voltage')))
                    .change(function(){
                        // Changes between test voltage and frequency forms
                        var sel = $('.test_type').val();
                        if (sel == 'freq') {
                            $('.test_div').replaceWith(test_select('Frequency', settings));
                        }
                        else if (sel == 'volt') {
                            $('.test_div').replaceWith(test_select('Voltage', settings));
                        }
                    }))
                    .append(test_select('Frequency',settings));
    };

    function test_select(item, settings) {
        var form = $('<form>').addClass('span2').attr('align', 'center')
        var field = $('<fieldset>')
                    .append('<label>Test '+item+' Value:</label>')
                    .append('<input class="start_'+item+'">').attr('type','text')
        return $('<div>').addClass('test_div').append(form.append(field)).append(run_button(settings, false, item))
    };

    function log_sweep(settings) {
        var form = $('<form>').addClass('span4')
        var field = $('<fieldset>')
                    .append('<legend>Log Frequency Sweep</legend>')
                    .append('<label>Start Decade</label>')
                    .append('<input class="start_Log">').attr('type','text')
                    .append('<label>Stop Decade</label>')
                    .append('<input class="stop_Log">').attr('type','text')
                    .append('<label>Number of Points in Decade</label>')
                    .append('<input class="step_Log">').attr('type','text')
        return $('<div>').addClass('sweep_div').append(form.append(field)).append(run_button(settings, true, 'Log'))
    };

    function status() {
        return $('<div>').addClass('span11 ')
                .addClass('progress')
                .append($('<div>').addClass('bar progress-bar')
                .css('width','1%'));
    };

    function run_button(settings, sweep, sweep_type) {
        return $('<div>').addClass('span12 button_div')
                .append($('<button>').addClass('span2 run-button').attr('align','left')
                .addClass('btn btn-primary').text('Run')
                .click(function(){
                    // sends all JS settings to kernel and converts them
                    // into python variables
                    var len = settings.length
                    for (var i=0;i<len;i++) {
                        var value = $(settings[i]).val()
                        IPython.notebook.kernel.execute(value)
                    };
                    // set the start, stop, and step frequency to 
                    // python dictionary
                    console.log(sweep)
                    if (sweep == false) {
                        console.log('.start_'+sweep_type)
                        var start = $('.start_'+sweep_type).val()
                        console.log(start)
                        IPython.notebook.kernel.execute('sweep["start"]='+start)
                        IPython.notebook.kernel.execute('sweep["sweep_type"]="'+sweep_type+'"')
                        IPython.notebook.kernel.execute('A,B,C = test_measurement(instr, panel, sweep)');
                    }
                    else if (sweep == null){}
                    else {
                        var start = $('.start_'+sweep_type).val()
                        var stop = $('.stop_'+sweep_type).val()
                        var step = $('.step_'+sweep_type).val()
                        IPython.notebook.kernel.execute('sweep["start"]='+start)
                        IPython.notebook.kernel.execute('sweep["stop"]='+stop)
                        IPython.notebook.kernel.execute('sweep["step"]='+step)
                        IPython.notebook.kernel.execute('sweep["sweep_type"]="'+sweep_type+'"')
                        if (sweep_type == 'Log'){
                            IPython.notebook.kernel.execute('A,B,C = log_sweep(instr, panel, sweep)')
                        } else {
                            IPython.notebook.kernel.execute('A,B,C = regular_sweep(instr, panel, sweep)')
                        }
                    };
                    IPython.notebook.kernel.execute('panel["osc_level"]='+$('.osc_level').val())

                    // grab the front panel settings in python and convert
                    // them to a message for the impedance analyzer
                    IPython.notebook.kernel.execute('pre_mess=grab_settings(panel)');
                    IPython.notebook.kernel.execute('message=message_to_analyzer(sweep_data,pre_mess)');
                    }));
    };

    /*
        This requires a webpage to have a div with id='AnalyzerUI' to build the UI.
    */

    var settings = ['.displayA','.displayB','.circuit','.trigger','.dcbias']

    $('#AnalyzerUI').append('<h3>Impedance Analyzer User Interface:</h3>')
        .append(sweep_select(settings))
        .append(select_box('Display A', 'displayA', ['Z/Y','R/G','L','C'], 4))
        .append(select_box('Display B', 'displayB', ['Rad','Deg'], 2))
        .append(select_box('Ciruit Mode', 'circuit', ['Auto', 'Parallel', 'Series'], 3))
        .append(select_box('Trigger', 'trigger', ['Hold/Manual', 'External', 'Internal'], 3))
        .append(switch_box('DC Bias','dcbias'))
        .append(switch_box('Append file','append'))
        .append(osc_level())
        .append($('<div>').addClass('span10').addClass('sweep_settings'))
        .append(no_sweep(settings))

    $('.displayA').change(function() {
        var sel = $('.displayA').val();
        if (sel == 'panel["displayA"]="Z/Y"' || sel == 'panel["displayA"]="R/G"') {
            $('.displayBdiv').replaceWith(select_box('Display B', 'displayB', ['Rad','Deg'], 2))
        } else if (sel == 'panel["displayA"]="L"' || sel == 'panel["displayA"]="C"') {
            $('.displayBdiv').replaceWith(select_box('Display B', 'displayB', ['Q','D','R/G'], 3))
        }

    });

    """)

panel={}
sweep={}

settings = dict(
    displayA = {'Z/Y':'A1,',
                'R/G':'A2,',
                'L':'A3,',
                'C':'A4,'},
    displayB = {'Deg':'B1,',
                'Rad':'B2,',
                'Q':'B1,',
                'D':'B2,',
                'R/G':'B3,'},
    log_sweep = {'On':'G0,', 
                 'Off':'G1,'},
    sweep_abort = {'On':'AB,'},
    sweep =     {'Off':'W0,', 
                 'On':'W1,'},
    manual_sweep = {'set_up':'W2,', 
                    'step_down': 'W1,'},
    circuit =   {'Auto':'C1,',
                 'Series':'C2,',
                 'Parallel':'C3,'},
    data_ready = {'On':'D1,',
                  'Off':'D0,'},
    output_data_format = {'A/B':'F0,',
                          'A/B/C':'F1,'},
    execute = {'execute':'EX,'},
    trigger = {'Internal':'T1,',
               'External':'T2,',
               'Hold/Manual':'T3,'},
    dcbias = {'Off':'I0,',
                'On': ''},
    sweep_mode = {'Frequency': '',
                    'Voltage Bias': '',
                    'Custom': ''},
    append = {'On': '',
                'Off': ''},
    osc_level = {}
    )


def sweep_message(sweep):
    """Creates and returns the string to send
    to the impedance analyzer for sweeps.

    Parameters
    ----------
    sweep: dict
        This dictionary holds all necessary information
        for a sweep.
        parameters:
            start: float
                starting value for the sweep
            stop: float
                stopping value for the sweep
            step: float
                the step size for each iteration
            sweep_type: str
                the type of sweep ('Frequency', 'Voltage')

    Returns
    -------
    message: str
        message string to commmunicate to the analyzer.
    iteration: int
        number of iterations in the sweep.
    """
    start = float(sweep['start'])
    stop = float(sweep['stop'])
    step = float(sweep['step'])
    if sweep['sweep_type'] == 'Frequency':
        message = "AB,W1,TF%.6fEN,PF%.6fEN,SF%.6fEN,G0,W2," %(start,stop,step)
    if sweep['sweep_type'] == 'Voltage':
        message = "AB,W1,TB%.2fEN,PB%.2fEN,SB%.2fEN,G0,W2," %(start,stop,step)
    iteration = int((stop - start)/step)
    return message, iteration

def test_message(sweep):
    """Creates and returns the string to send
    to the impedance analyzer for test measurements.

    Parameters
    ----------
    test_data: dict
        This dictionary holds all necessary information
        for a sweep.
        parameters:
            start: float
                starting value for the sweep
            sweep_type: str
                the type of sweep ('Frequency', 'Voltage')
    Returns
    -------
    message: str
        message string to commmunicate to the analyzer.
    """
    start = float(sweep['start'])
    if sweep['sweep_type'] == 'Frequency':
        message = "FR%.6fEN," %(start)
    if sweep['sweep_type'] == 'Voltage':
        message = "BI%.2fEN," %(start)
    return message

def grab_settings(panel):
    """Takes a dictionary containing the settings for
    the front panel of an HP4192A LF impedance analyzer
    and returns an concatenated string message to be 
    written to the machine.
    Parameters
    ----------
        panel: dict
            dict of all the desired settings for the analyzer.
            
    Returns
    -------
        message: str
            A message string that contains the appropriate
            syntax for the analyzer.
    """
    message = ''
    for p in panel:
        if p != 'osc_level':
            message+= settings[p][panel[p]]
    message += "OL%.3fEN," %float(panel['osc_level'])
    return message

def message_to_analyzer(frequency='', *args):
    """Concatenates the full string message (with 
    sweep information) to send to the analyzer"""
    pre = "RL1,D1,R8,F1,%s" %args
    message = pre + frequency + 'EX'
    return message

def read_message(message, C=False):
    """Parses the response message (must be given) from the 
    analyzer and returns the values for display A, display B,
    and (if C=True) display C"""
    A = message[4:15]
    B = message[20:31]
    if C is True:
        C = message[33:43]
        return A,B,C
    else:
        return A,B

def test_measurement(instr, panel, data):
    """Runs a test measurment with the analyzer.
    
    Parameters
    ----------
        instr:
            The VISA instrument object for the 
            impedance analyzer.
        panel: dict
            A dictionary that holds the settings from
            the front panel of the machine.
        data: dict
            The dictionary that holds all settings
            for the test measurment.
        
    Returns
    -------
        A: float
            The value for display A from the test.
        B: float
            The value for display B from the test.
        C: float
            The value for display C from the test.
    """
    message = grab_settings(panel)
    test = test_message(data)
    message = message_to_analyzer(test, message)
    instr.write(message)
    m = instr.read()
    displays = read_message(m, True)
    A.append(displays[0])
    B.append(displays[1])
    C.append(displays[2])
    return A, B, C
    

def regular_sweep(instr, panel, sweep):
    """Runs a standard sweep with the analyzer.
    
    Parameters
    ----------
        instr:
            The VISA instrument object for the 
            impedance analyzer.
        panel: dict
            A dictionary that holds the settings from
            the front panel of the machine.
        sweep: dict
            The dictionary that holds all settings
            for the sweep. (see 'sweep_message docs')
    Returns
    -------
        A: list
            The values for display A from the sweep.
        B: list
            The values for display B from the sweep.
        C: list
            The values for display C from the sweep.
    """
    message = grab_settings(panel)
    sweep, i = sweep_message(sweep)
    message = message_to_analyzer(sweep, message)
    instr.write(message)
    A = []
    B = []
    C = []
    for j in range(0,i,1):
        m = instr.read()
        displays = read_message(m,True)
        A.append(displays[0])
        B.append(displays[1])
        C.append(displays[2])
    return A, B, C

def log_sweep(n, first_decade, last_decade):
    """Runs a log sweep between the two given decades.
    
    Parameters
    ----------
        n: int
            number of points between each decade in for a log sweep.
        first_decade: int
            the decade exponent number to start the sweep.
            (i.e. 4 if you mean '10^4')
        last_decade: int
            the decade exponent number to stop the sweep.
            (i.e. 4 if you mean '10^4')

    Returns
    -------
        A: list
            The values for display A from the sweep.
        B: list
            The values for display B from the sweep.
        C: list
            The values for display C from the sweep.
    """
    A = []
    B = []
    C = []
    start = int(log10(first_decade))
    stop = int(log10(last_decade))
    for j in range(start, stop):
        steps = float((10**(j+1)-10**(j))/n)
        freq, i = freq_range(10**j, 10**(j+1), steps)
        message = message_to_analyzer(freq, settings())
        instr.write(message)
        for j in range(0,i,1):
            m = instr.read()
            displays = read_message(m,True)
            A.append(displays[0])
            B.append(displays[1])
            C.append(displays[2])
        time.sleep(2)
    return A, B, C