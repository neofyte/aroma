//
// showdown-gui.js
//
// A sample application for Showdown, a javascript port
// of Markdown.
//
// Copyright (c) 2007 John Fraser.
//
// Redistributable under a BSD-style open source license.
// See license.txt for more information.
//
// The full source distribution is at:
//
//				A A L
//				T C A
//				T K B
//
//   <http://www.attacklab.net/>
//

//
// The Showdown converter itself is in showdown.js, which must be
// included by the HTML before this file is.
//
// showdown-gui.js assumes the id and class definitions in
// showdown.html.  It isn't dependent on the CSS, but it does
// manually hide, display, and resize the individual panes --
// overriding the stylesheets.
//
// This sample application only interacts with showdown.js in
// two places:
//
//  In startGui():
//
//      converter = new Showdown.converter();
//
//  In convertText():
//
//      text = converter.makeHtml(text);
//
// The rest of this file is user interface stuff.
//


//
// Register for onload
//
window.onload = startGui;


//
// Globals
//

var converter;
var convertTextTimer,processingTime;
var lastText,lastRoomLeft;
var inputPanel,previewPanel,outputPane,syntaxPane;
var maxDelay = 3000; // longest update pause (in ms)


//
//	Initialization
//

function startGui() {
	// find elements
	inputPanel = document.getElementById("inputPanel");
	previewPanel = document.getElementById("previewPanel");

	

	// First, try registering for keyup events
	// (There's no harm in calling onInput() repeatedly)
	window.onkeyup = inputPanel.onkeyup = onInput;

	// In case we can't capture paste events, poll for them
	var pollingFallback = window.setInterval(function(){
		if(inputPanel.value != lastText)
			onInput();
	},1000);

	// Try registering for paste events
	inputPanel.onpaste = function() {
		// It worked! Cancel paste polling.
		if (pollingFallback!=undefined) {
			window.clearInterval(pollingFallback);
			pollingFallback = undefined;
		}
		onInput();
	}

	// Try registering for input events (the best solution)
	if (inputPanel.addEventListener) {
		// Let's assume input also fires on paste.
		// No need to cancel our keyup handlers;
		// they're basically free.
		inputPanel.addEventListener("input",inputPanel.onpaste,false);
	}


	// start with blank page?
	if (top.document.location.href.match(/\?blank=1$/))
		inputPanel.value = "";

	// build the converter
	converter = new Showdown.converter();

	// do an initial conversion to avoid a hiccup
	convertText();

	// give the input pane focus
	inputPanel.focus();

	// start the other panes at the top
	// (our smart scrolling moved them to the bottom)
	previewPanel.scrollTop = 0;
}


//
//	Conversion
//

function convertText() {
	// get input text
	var text = inputPanel.value;
	
	// if there's no change to input, cancel conversion
	if (text && text == lastText) {
		return;
	} else {
		lastText = text;
	}

	var startTime = new Date().getTime();

	// Do the conversion
	text = converter.makeHtml(text);

	//var math = MathJax.Hub.getAllJax(text)[0];
	//MathJax.Hub.Queue(["Typeset",MathJax.Hub,math]);

	// display processing time
	var endTime = new Date().getTime();	
	processingTime = endTime - startTime;

	// save proportional scroll positions
	saveScrollPositions();

	// update right pane
		// the preview pane is selected
	previewPanel.innerHTML = text;

	var math = MathJax.Hub.getAllJax(previewPanel.innerHTML)[0];
	MathJax.Hub.Queue(["Typeset",MathJax.Hub,math]);

	// restore proportional scroll positions
	restoreScrollPositions();

};


//
//	Event handlers
//

function onInput() {
// In "delayed" mode, we do the conversion at pauses in input.
// The pause is equal to the last runtime, so that slow
// updates happen less frequently.
//
// Use a timer to schedule updates.  Each keystroke
// resets the timer.

	// if we already have convertText scheduled, cancel it
	if (convertTextTimer) {
		window.clearTimeout(convertTextTimer);
		convertTextTimer = undefined;
	}

		var timeUntilConvertText = 0;
			// make timer adaptive
		timeUntilConvertText = processingTime;

		if (timeUntilConvertText > maxDelay)
			timeUntilConvertText = maxDelay;

		// Schedule convertText().
		// Even if we're updating every keystroke, use a timer at 0.
		// This gives the browser time to handle other events.
		convertTextTimer = window.setTimeout(convertText,timeUntilConvertText);
}



//
// Smart scrollbar adjustment
//
// We need to make sure the user can't type off the bottom
// of the preview and output pages.  We'll do this by saving
// the proportional scroll positions before the update, and
// restoring them afterwards.
//

var previewScrollPos;

function getScrollPos(element) {
	// favor the bottom when the text first overflows the window
	if (element.scrollHeight <= element.clientHeight)
		return 1.0;
	return element.scrollTop/(element.scrollHeight-element.clientHeight);
}

function setScrollPos(element,pos) {
	element.scrollTop = (element.scrollHeight - element.clientHeight) * pos;
}

function saveScrollPositions() {
	previewScrollPos = getScrollPos(previewPanel);
}

function restoreScrollPositions() {
	// hack for IE: setting scrollTop ensures scrollHeight
	// has been updated after a change in contents
	previewPanel.scrollTop = previewPanel.scrollTop;

	setScrollPos(previewPanel,previewScrollPos);
}