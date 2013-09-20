#from pyvisa.vpp43 import visa_library
#visa_library.load_library(r"C:\Windows\System32\visa32.dll")
#import visa
#instr = visa.instrument("GPIB3::17::INSTR")
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
    
    function sweep_select() {
        return $('<div>').attr('align','right').addClass('span3').text('Type of Sweep:')
                .append($('<select/>').addClass('span3 switch-box').addClass('sweep_type')
                    .append(($('<option>').val('noFreq').text('No Sweep')))
                    .append(($('<option>').val('regFreq').text('Regular Frequency Sweep')))
                    .append(($('<option>').val('logFreq').text('Log Frequency Sweep')))
                    .append(($('<option>').val('regVolt').text('Voltage Bias Sweep')))
                    .append(($('<option>').val('custsweep').text('Custom Sweep'))));           
    }
    
    function switch_box(name, variable) {
        return $('<div>').attr('align','right').addClass('span3').text(name+': ')
                .append($('<select/>').addClass('span3 switch-box').addClass(variable)
                .append(($('<option>').val('panel["'+ variable + '"]="On"').text('ON')))
                .append(($('<option>').val('panel["'+ variable + '"]="Off"').text('OFF'))));
    }

    function select_box(name, item, variable, len) {
        var box = $('<div>').attr('align','right').addClass('span3').text(name+': ')
        var select = $('<select>').addClass('span3 select-box').addClass(item)
        for (var i=0;i<len;i++) {
            select = select.append($('<option>')
            .val('panel["'+ item + '"]='+variable[i]).text(variable[i]))
        };
        return box.append(select);
    };

    function reg_sweep(item, settings){
        var form = $('<form>').addClass('span4')
        var field = $('<fieldset>')
                    .append('<legend>'+item+' Sweep</legend>')
                    .append('<label>Start '+item+'</label>')
                    .append('<input class="start_'+item+'">').attr('type','text')
                    .append('<label>Stop '+item+'</label>')
                    .append('<input class="stop_'+item+'">').attr('type','text')
                    .append('<label>Step '+item+'</label>')
                    .append('<input class="step_'+item+'">').attr('type','text')
        return $('<div>').addClass('sweep_div').append(form.append(field)).append(run_button(settings, item))
    };

    function no_sweep(settings){
        var form = $('<form>').addClass('span4')
        var field = $('<fieldset>')
                    .append('<label>Test Frequency:</label>')
                    .append('<input class="start_frequency">').attr('type','text')
        return $('<div>').addClass('sweep_div').append(form.append(field)).append(run_button(settings, false))
    };
    
    function log_sweep(settings){
        var form = $('<form>').addClass('span4')
        var field = $('<fieldset>')
                    .append('<legend>Log Frequency Sweep</legend>')
                    .append('<label>Start Decade</label>')
                    .append('<input class="start_frequency">').attr('type','text')
                    .append('<label>Stop Decade</label>')
                    .append('<input class="stop_frequency">').attr('type','text')
                    .append('<label>Number of Points in Decade</label>')
                    .append('<input class="step_frequency">').attr('type','text')
        return $('<div>').addClass('sweep_div').append(form.append(field)).append(run_button(settings, 'Frequency'))
    };

    function status() {
        return $('<div>').addClass('span11 ')
                .addClass('progress')
                .append($('<div>').addClass('bar progress-bar')
                .css('width','1%'));

    };

    function run_button(settings, sweep) {
        return $('<div>').addClass('span12 button_div')
                .append($('<button>').addClass('span2 run-button')
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
                    // python variables
                    if (sweep == false) {
                        var start = $('.start_'+sweep).val()
                        IPython.notebook.kernel.execute('start='+start)
                    }
                    else if (sweep == null){}
                    else {
                        var start = $('.start_'+sweep).val()
                        var stop = $('.stop_'+sweep).val()
                        var step = $('.step_'+sweep).val()
                        IPython.notebook.kernel.execute('start='+start)
                        IPython.notebook.kernel.execute('stop='+stop)
                        IPython.notebook.kernel.execute('step='+step)
                        var gap = stop-start;
                        IPython.notebook.kernel.execute('sweep_data,it=freq_range(start,stop,step)');
                    };
                
                    // grab the front panel settings in python and convert
                    // them to a message for the impedance analyzer
                    IPython.notebook.kernel.execute('pre_mess=grab_settings(panel)');
                    IPython.notebook.kernel.execute('message=message_to_analyzer(sweep_data,pre_mess)');
                    }));
    };

    var settings = ['.displayA','.displayB','.circuit','.trigger',
                    '.sweep','.dcbias','.sweep_mode','.append']

    $('#AnalyzerUI').append('<h3>Impedance Analyzer:</h3>')
        .append(sweep_select())
        .append(select_box('Display A', 'displayA', ['"Z/Y"','"R/G"','"L"','"C"'], 4))
        .append(select_box('Display B', 'displayB', ['"Rad"','"Deg"','"C"'], 3))
        .append(select_box('Ciruit Mode', 'circuit', ['"Parallel"', '"Series"', '"Auto"'], 3))
        .append(select_box('Trigger', 'trigger', ['"Hold/Manual"', '"External"', '"Internal"'], 3))
        .append(switch_box('Sweep','sweep'))
        .append(switch_box('DC Bias','dcbias'))
        .append(select_box('Sweep mode', 'sweep_mode', ['"Frequency"', '"Voltage Bias"', '"Custom"'], 3))
        .append(switch_box('Append file','append'))
        .append($('<div>').addClass('span10').addClass('sweep_settings'))
        .append($('<div>').addClass('sweep_div').append(no_sweep(settings)))
        
    $('.sweep_type').change(function(){
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
            $('.sweep_div').replaceWith($('<div>').addClass('sweep_div').append(run_button(settings, null)));

        }
    })
    """)

panel={}

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
                'Off': ''}
    )


def freq_range(start, stop, steps):
    """Creates and returns the string to send
    to the impedance analyzer for frequency sweeps.

    Parameters
    ----------
    start: float
        starting frequency for a frequency sweep.
    stop: float
        frequency for the sweep to stop at.
    step: float
        the step between each frequency measurement.

    Returns
    -------
    freq: str
        string for frequency sweep.
    iteration: int
        number of frequency iterations.
    """
    start= float(start)
    stop = float(stop)
    steps = float(steps)
    freq = "AB,W1,TF%.6fEN,PF%.6fEN,SF%.6fEN,G0,W2," %(start,stop,steps)
    iteration = int((stop - start)/steps)
    return freq, iteration

def grab_settings(panel):
    """Takes a dictionary containing the settings for
    the front panel of an HP4192A LF impedance analyzer
    and returns an concatenated messaging string to be 
    written to the machine.
    """
    message = ''
    for p in panel:
        message+= settings[p][panel[p]]
    return message

def message_to_analyzer(frequency, *args):
    pre = "RL1,D1,R8,F1,%s" %args
    message = pre + frequency +'EX'
    return message

def read_message(message, C=False):
    A = message[4:15]
    B = message[20:31]
    if C is True:
        C = message[33:43]
        return A,B,C
    else:
        return A,B

def regular_sweep(instr):
    instr.write(message)
    A = []
    B = []
    for j in range(0,i,1):
        m = instr.read()
        displays = read_message(m,False)
        A.append(displays[0])
        B.append(displays[1])

def log_sweep_plot(n, first_decade, last_decade):
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