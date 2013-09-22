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