
(function (ns) {
    var views = ns.views,
        models = ns.models,
        templates = ns.templates;

    views.Index = Backbone.View.extend({

        model: {
            screenshots: [
                {'img': 'something', 'name': 'A name'},
                {'img': 'another', 'name': 'Another name'}
            ]
        },

        template: templates.index,

        events: {
            "click .submit": "saveEvent"
        },

        render: function () {
            console.log('Rendering index view', this.template, this.model);
            $(this.el).html(Mustache.render(this.template, this.model))
        },

        saveEvent: function (e) {
            alert(e.target.tagName);
            e.preventDefault();
        }
    });

 })(debitor);
