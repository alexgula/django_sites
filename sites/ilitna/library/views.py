# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from navigation.views import HomeNavigationView, NavigationDetailView, NavigationListView
from navigation.models import StaticNode
from .models import Author, Work, Publisher, Publication


class AuthorListView(NavigationListView):
    model = Author
    trail_parent = HomeNavigationView
    trail = StaticNode(_("Authors"), 'library:author_list')

    def get_queryset(self):
        return super(AuthorListView, self).get_queryset().filter(active=True).prefetch_related('work_set')


class AuthorDetailView(NavigationDetailView):
    model = Author
    trail_parent = AuthorListView

    def get_trail_nodes(self):
        trail = super(AuthorDetailView, self).get_trail_nodes()
        return trail + [self.object]


class WorkListView(NavigationListView):
    model = Work
    trail_parent = HomeNavigationView
    trail = StaticNode(_("Works"), 'library:work_list')

    def get_queryset(self):
        return Work.objects.listed()


class WorkDetailView(NavigationDetailView):
    model = Work
    trail_parent = WorkListView
    slug_field = 'slug_trail'

    def get_trail_nodes(self):
        trail = super(WorkDetailView, self).get_trail_nodes()
        return trail + [self.object.get_ancestors()] + [self.object]

    def get_context_data(self, **kwargs):
        context = super(WorkDetailView, self).get_context_data(**kwargs)

        root = self.object.get_root()

        work_children = list(self.object.get_children())
        if len(work_children) == 0:
            next_work = self.object.get_next_sibling()
            if next_work is None:
                current_work = self.object
                while current_work <> root and next_work is None:
                    current_work = current_work.parent
                    next_work = current_work.get_next_sibling()
        else:
            next_work = work_children[0]

        prev_work_sibling = self.object.get_previous_sibling()
        if prev_work_sibling is None:
            prev_work = self.object.parent
        else:
            prev_work_sibling_descendants = list(prev_work_sibling.get_descendants())
            if len(prev_work_sibling_descendants) == 0:
                prev_work = prev_work_sibling
            else:
                prev_work = prev_work_sibling_descendants[-1]

        context['root'] = root
        context['next'] = next_work
        context['prev'] = prev_work
        context['has_children'] = len(work_children) > 0
        return context


class PublisherListView(NavigationListView):
    model = Publisher
    trail_parent = HomeNavigationView
    trail = StaticNode(_("Publishers"), 'library:publisher_list')

    def get_queryset(self):
        return super(PublisherListView, self).get_queryset().filter(active=True)


class PublisherDetailView(NavigationDetailView):
    model = Publisher
    trail_parent = PublisherListView

    def get_trail_nodes(self):
        trail = super(PublisherDetailView, self).get_trail_nodes()
        return trail + [self.object]


class PublicationListView(NavigationListView):
    model = Publication
    trail_parent = HomeNavigationView
    trail = StaticNode(_("Publications"), 'library:publication_list')

    def get_queryset(self):
        return super(PublicationListView, self).get_queryset().filter(active=True)


class PublicationDetailView(NavigationDetailView):
    model = Publication
    trail_parent = PublicationListView

    def get_trail_nodes(self):
        trail = super(PublicationDetailView, self).get_trail_nodes()
        return trail + [self.object]
