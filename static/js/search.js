$(document).ready(function() {
    var elements_selected = {};
    var platforms_selected = {};

    var add_element = function(id, text) {
        var item = $('<li class="' + id + '">'+text+'</li>');
        $('#search-criteria').append(item);
    }
    var remove_element = function(id) {
        $('#search-criteria .' + id).remove();
    }


    $('[name="elements-selected"]').on('change', function(){
        if (this.checked) {
            elements_selected[this.id] = this.labels[0].innerText.replace(/^\s+|\s+$/g, '');
            add_element(this.id, elements_selected[this.id]);
        } else {
            delete elements_selected[this.id];
            remove_element(this.id);
        }
        console.log(elements_selected);
    })

    $('[name="platforms-selected"]').on('change', function(){
        if (this.checked) {
            elements_selected[this.id] = this.labels[0].innerText.replace(/^\s+|\s+$/g, '');
            add_element(this.id, elements_selected[this.id]);
        } else {
            delete elements_selected[this.id];
            remove_element(this.id);
        }
        console.log(elements_selected);
    })
});