
var hot = null;
var csrftoken = null;

function replaceTag(tag) {
	var tagsToReplace = {
		'&': '&amp;',
		'<': '&lt;',
		'>': '&gt;'
	};
	console.log('replaceTag',tag);
	return tagsToReplace[tag] || tag;
}
function safe_tags_replace(str) {
	//console.log('safe_tags_replace',str);
	return str.replace(/[&<>]/g, replaceTag);
}
function customRenderer (instance, td, row, col, prop, value, cellProperties) {
	//console.log('customRenderer');
	//console.log('  value      ',value);
	//console.log('  value type ',typeof value);

	var v = null;

	if(typeof value == 'string') {
		console.log('renderer got string value');
		console.log(value);
		v = value;

		//console.log('error!');
		//alert('error!');
		
		//var j = JSON.parse(value);
		//var j = value;

		//console.log('  object     ',j);
		//var escaped = Handsontable.helper.stringify(j[1]);
		//var escaped = escape(j[1]);
		//var escaped = j[1];
		//var escaped = safe_tags_replace(j[1]);
		//console.log('  escaped    ',escaped);
		//v = escaped;
     	} else if(value == null) {
		//console.log('renderer: value is null');
		// encountered when dragging to create new rows
		v = '';
	} else if(typeof value == 'object') {
		v = value[1];
	} else {
		console.log('error!');
		console.log('value:', value);
	}

	td.innerHTML = v;

	//console.log('display');
	//console.log(v);

	//Handsontable.renderers.TextRenderer.apply(this, arguments);
}

function apply_data(data_new) {
	//console.log(data_new.cells);

	data.splice(0,data.length);

	data_new.cells.forEach(function(c) {
		//console.log('push');
		//console.log(c);
		var c_new = c.map(function(e) {
			return JSON.parse(e);
		});
		//console.log(c_new);
		data.push(c_new);
	});

	hot.render();
}
function apply_sheet_data(data_new) {
	console.log('apply_sheet_data', data_new);
        apply_data(data_new);
        $("#script").val(data_new.script_pre);
        $("#script_output").val(data_new.script_pre_output);
}
function add_column() {
	var post_data = {
		"sheet_key": sheet_key,
		'i': null, 
		'csrfmiddlewaretoken': csrftoken
	};
	$.post(url_add_column, post_data, apply_data);
}
function add_row() {
	var post_data = {
		"sheet_key": sheet_key,
		'i': null, 
		'csrfmiddlewaretoken': csrftoken
	};
	$.post(url_add_row, post_data, apply_data);
}
function get_sheet_data() {
        var post_data = {
		'csrfmiddlewaretoken':csrftoken,
		'sheet_key': sheet_key,
	};
	var jqxhr = $.post(url_get_sheet_data, post_data, apply_sheet_data).fail(function() {
		alert("get sheet data ajax post fail");
	});
}
function set_script_pre() {
	//console.log('set script pre ' + url_set_script_pre);
	var text = $("#script").val();
        var post_data = {
		'csrfmiddlewaretoken':csrftoken,
		"sheet_key": sheet_key,
		'text':text 
	};
	var jqxhr = $.post(url_set_script_pre, post_data, apply_sheet_data);
	jqxhr.done(function() {
		//alert("set script pre ajax post success");
	});
	jqxhr.fail(function() {
		alert("set script pre ajax post fail");
	});
}
function sheet_page_load() {

	csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

	var container = document.getElementById('tablediv');

	var hooks = Handsontable.hooks.getRegistered();

	console.log(hooks);

	hot = new Handsontable(container, {
		data: data,
		rowHeaders: true,
		colHeaders: true,
		cells: function (row, col, prop) {
			this.renderer = customRenderer;
		}
		//columns: [{renderer:customRenderer}]
	});

	hooks.forEach(function(h) {
		var ignore = [
			"beforeOnCellMouseOver",
			"afterOnCellMouseOver",
			"beforeOnCellMouseOut",
			"afterOnCellMouseOut",
			"beforeOnCellMouseDown",
			"afterOnCellMouseDown",
			"beforeDrawBorders",
			"modifyColWidth",
			"modifyRowHeaderWidth",
			"afterGetRowHeaderRenderers",
			"afterGetColumnHeaderRenderers",
			"afterDocumentKeyDown",
			"beforeKeyDown",
		];

		//if(ignore.indexOf(h) > -1) return;
		return
		
		hot.addHook(h, function() {
			console.log(h);
		});
	});

	hot.addHook('beforeCopy', function(data, coords) {
		console.log('beforeCopy');
		console.log(data);
		console.log(coords);
		/*
		var d = arguments[0].map(function(r){
			return r.map(function(c){
				return c[0];
			});
		});*/
		var data_new = data.map(function(c){
			return c.map(function(v){
				console.log(v);
				return v[0];
			})
		});

		console.log(data_new);

		data.splice(0,data.length);
	
		data_new.forEach(function(c) {
			data.push(c);
		});

	});

	hot.addHook('afterCopy', function(data, coords) {
		console.log('afterCopy');
		console.log(data);
	});

	hot.addHook('modifyData', function() {
		if(arguments[3] == 'set') {
			console.log('modifyData -----------------------');
			console.log(arguments);
			//var o = arguments[2];
			//o.value = JSON.stringify([o.value,'']);
		}
	});

	hot.addHook('afterSetDataAtCell', function() {
		console.log('afterSetDataAtCell -----------------------');
		console.log(arguments);
	});

	hot.addHook('beforeValidate', function() {
		console.log('beforeValidate -----------------------');
	});

	hot.addHook('afterValidate', function() {
		console.log('afterValidate -----------------------');
	});

	hot.addHook('afterBeginEditing', function() {
		console.log('afterBeginEditing ------------------------');
		console.log(arguments);
		r = arguments[0];
		c = arguments[1];
		d = data[r][c];
		//console.log(d);
		//data[r][c] = 'hello';
		//hot.render();
	});
	hot.addHook('afterChange', function() {
		console.log('afterChange ------------------------');
		arguments[0].forEach(function(args) {
			console.log(args);

			var post_data = {
				"sheet_key": sheet_key,
				'csrfmiddlewaretoken': csrftoken,
				'r': args[0],
				'c': args[1],
				's': args[3]
			};

			$.post(url_set_cell, post_data, apply_data);
		});
	});

	get_sheet_data();
}

