function changePlus(node)
{
	var child = node.children[0];
	if (child.classList.contains('fa-plus'))
	{
		child.classList.remove("fa-plus");
		child.classList.add("fa-minus");
	}
	else{
		child.classList.remove("fa-minus");
		child.classList.add("fa-plus");
	}
}

function changeRemoveButton(node)
{
	var child = node.children[0];
	if (child.style.color == 'rgb(206, 78, 61)')
	{
		child.style.color ="#5C3901";
	}
	else{
		child.style.color ="#CE4E3D";
	}
}
