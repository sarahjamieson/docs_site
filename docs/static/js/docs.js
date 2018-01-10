$(document).ready(function(){

    // training.html - dom code swaps search box and page length.
    $('#training-table').DataTable({
        "order": [[1, "asc"], [0, "asc"], [2, "asc"]],
        'dom': '<"pull-left"f><"pull-right"l>t<"pull-left"i><"pull-right"p>',
    });

    // ngs.html and data.html - Ajax to copy text to clipboard
    $(document).on('click', 'span.glyphicon-copy', function(e) {
        var doc = this.id;

        $.ajax({
            url: '/docs/ajax_copy/',
            type: 'get',
            data: {'doc': doc},
            success: function(data){
                $("#msg").html(data);
            }
        });
    });

    // ngs.html - Ajax to select circle and display docs for selection
    $(document).on('click', 'circle.selectableCircle', function(e) {
        var test = this.id;

        var all_circles = document.getElementsByClassName('selectableCircle');
        for (var i=0, il=all_circles.length; i<il; i++){
            all_circles[i].style.fill = '#fff';
        }

        var circle = document.getElementById(test);

        circle.style.fill = 'lightsteelblue';

        $.ajax({
            url: '/docs/ajax_test_docs/',
            type: 'get',
            data: {'name': test},
            success: function(data){
                $("#show_docs").html(data);
            }
        });
    });
});

