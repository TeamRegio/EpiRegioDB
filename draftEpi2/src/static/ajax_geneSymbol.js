$(function(){
    $('#geneID_symbolic').keyup(function(){

        $.ajax({
            type: "POST",
            url: "/genesymbol_search",
            data: {
                'search_text_gene': $('#geneID_symbolic').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
            success: searchSuccessGene,
            dataType: 'html',
            id: 'search-results-gene'
            });
        });
})

function searchSuccessGene(data, textStatus, jqXHR)
{
    $('#search-results-gene').html(data);
}