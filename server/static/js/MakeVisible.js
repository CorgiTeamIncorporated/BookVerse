function MakeVisible(id){
	var inputBox = document.querySelector('#'+id);
	if (inputBox.style.visibility == "hidden")
	{
		inputBox.style.visibility = "visible"
		inputBox.style.removeProperty('height');
	}
	else
	{
		inputBox.style.visibility = "hidden"
		inputBox.style.height = "0px"
	}
}
