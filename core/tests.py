from unittest.mock import MagicMock

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase

from adminsortable2.admin import SortableAdminMixin

from .admin import ProjectAdmin, PublicationAdmin, SkillAdmin
from .models import Project, Publication, Skill


# ── helpers ────────────────────────────────────────────────────────────────────

def make_project(title, order=0):
    return Project.objects.create(title=title, description='d', order=order)


def make_skill(name, category=Skill.LANGUAGES, order=0):
    return Skill.objects.create(name=name, category=category, order=order)


# ── Class 1: old collision behaviour (documentation tests) ────────────────────

class OldOrderingCollisionTests(TestCase):
    """
    Show what happens at the model layer with default order=0.
    These tests bypass the admin to reproduce the original broken state.
    They pass both before and after the fix — they document the behaviour
    that the admin mixin prevents during normal use.
    """

    def test_two_projects_at_order_zero_sort_alphabetically(self):
        make_project('Zebra Project', order=0)
        make_project('Alpha Project', order=0)
        titles = list(Project.objects.values_list('title', flat=True))
        # Both at order=0: Meta fallback to 'title' decides the sequence.
        self.assertEqual(titles, ['Alpha Project', 'Zebra Project'])

    def test_two_skills_at_order_zero_sort_alphabetically_within_category(self):
        make_skill('Python', order=0)
        make_skill('Go', order=0)
        names = list(
            Skill.objects.filter(category=Skill.LANGUAGES).values_list('name', flat=True)
        )
        # Both at order=0: Meta fallback to 'name' decides the sequence.
        self.assertEqual(names, ['Go', 'Python'])

    def test_inserting_between_two_items_requires_manual_renumber(self):
        """Duplicate order values cause tie-breaking by title, not intended position."""
        make_project('A', order=1)
        original_b = make_project('B', order=2)
        make_project('C', order=3)

        # Insert 'B-New' at order=2 without renumbering — creates a collision.
        make_project('B-New', order=2)
        titles = list(Project.objects.values_list('title', flat=True))
        # 'B' and 'B-New' both have order=2; tie-broken alphabetically.
        self.assertEqual(titles, ['A', 'B', 'B-New', 'C'])

        # To fix, the author must manually shift subsequent items.
        original_b.order = 3
        original_b.save()
        Project.objects.filter(title='C').update(order=4)
        titles = list(Project.objects.values_list('title', flat=True))
        self.assertEqual(titles, ['A', 'B-New', 'B', 'C'])


# ── Class 2: ProjectAdmin auto-append ─────────────────────────────────────────

class ProjectAutoAppendTests(TestCase):
    """
    SortableAdminMixin.save_model assigns max_order + 1 when change=False.
    We call it directly to test without a real HTTP request.
    """

    def setUp(self):
        self.site = AdminSite()
        self.admin = ProjectAdmin(Project, self.site)

    def _create_via_admin(self, title):
        obj = Project(title=title, description='d')
        self.admin.save_model(MagicMock(), obj, MagicMock(), change=False)
        return obj

    def test_first_project_gets_order_1(self):
        p = self._create_via_admin('First')
        self.assertEqual(p.order, 1)

    def test_second_project_gets_order_2(self):
        self._create_via_admin('First')
        p2 = self._create_via_admin('Second')
        self.assertEqual(p2.order, 2)

    def test_third_project_gets_order_3(self):
        self._create_via_admin('First')
        self._create_via_admin('Second')
        p3 = self._create_via_admin('Third')
        self.assertEqual(p3.order, 3)

    def test_order_values_are_unique_after_four_creates(self):
        for t in ['Alpha', 'Beta', 'Gamma', 'Delta']:
            self._create_via_admin(t)
        orders = list(Project.objects.values_list('order', flat=True))
        self.assertEqual(len(orders), len(set(orders)))

    def test_appends_after_highest_existing_order(self):
        make_project('Manual', order=10)
        p_new = self._create_via_admin('AutoAppend')
        self.assertEqual(p_new.order, 11)

    def test_editing_does_not_change_order(self):
        p = self._create_via_admin('First')
        original_order = p.order
        self.admin.save_model(MagicMock(), p, MagicMock(), change=True)
        self.assertEqual(p.order, original_order)


# ── Class 3: SkillAdmin auto-append with per-category scoping ─────────────────

class SkillAutoAppendTests(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.admin = SkillAdmin(Skill, self.site)

    def _create_skill_via_admin(self, name, category):
        obj = Skill(name=name, category=category)
        self.admin.save_model(MagicMock(), obj, MagicMock(), change=False)
        return obj

    def test_first_skill_in_languages_gets_order_1(self):
        s = self._create_skill_via_admin('Python', Skill.LANGUAGES)
        self.assertEqual(s.order, 1)

    def test_second_skill_in_languages_gets_order_2(self):
        self._create_skill_via_admin('Python', Skill.LANGUAGES)
        s2 = self._create_skill_via_admin('Go', Skill.LANGUAGES)
        self.assertEqual(s2.order, 2)

    def test_first_skill_in_new_category_resets_to_1(self):
        self._create_skill_via_admin('Python', Skill.LANGUAGES)
        self._create_skill_via_admin('Go', Skill.LANGUAGES)
        fw = self._create_skill_via_admin('Django', Skill.FRAMEWORKS)
        self.assertEqual(fw.order, 1)

    def test_second_skill_in_second_category_gets_order_2(self):
        self._create_skill_via_admin('Python', Skill.LANGUAGES)
        self._create_skill_via_admin('Django', Skill.FRAMEWORKS)
        fw2 = self._create_skill_via_admin('FastAPI', Skill.FRAMEWORKS)
        self.assertEqual(fw2.order, 2)

    def test_languages_sequence_unaffected_by_frameworks_inserts(self):
        self._create_skill_via_admin('Python', Skill.LANGUAGES)
        self._create_skill_via_admin('Django', Skill.FRAMEWORKS)
        self._create_skill_via_admin('Go', Skill.LANGUAGES)
        lang_pairs = list(
            Skill.objects.filter(category=Skill.LANGUAGES)
                         .order_by('order')
                         .values_list('name', 'order')
        )
        self.assertEqual(lang_pairs, [('Python', 1), ('Go', 2)])

    def test_all_four_categories_maintain_independent_sequences(self):
        for cat in [Skill.LANGUAGES, Skill.FRAMEWORKS, Skill.CONCEPTS, Skill.SOFT_SKILLS]:
            self._create_skill_via_admin(f'skill-1', cat)
            self._create_skill_via_admin(f'skill-2', cat)
        for cat in [Skill.LANGUAGES, Skill.FRAMEWORKS, Skill.CONCEPTS, Skill.SOFT_SKILLS]:
            orders = list(
                Skill.objects.filter(category=cat)
                             .order_by('order')
                             .values_list('order', flat=True)
            )
            self.assertEqual(orders, [1, 2], f'{cat} should have orders [1, 2]')


# ── Class 4: queryset ordering correctness ────────────────────────────────────

class ProjectQuerysetOrderingTests(TestCase):

    def test_projects_ordered_by_order_then_title(self):
        make_project('B', order=2)
        make_project('A', order=1)
        make_project('C', order=3)
        self.assertEqual(
            list(Project.objects.values_list('title', flat=True)),
            ['A', 'B', 'C'],
        )

    def test_equal_order_values_fall_back_to_title(self):
        make_project('Z', order=5)
        make_project('A', order=5)
        self.assertEqual(
            list(Project.objects.values_list('title', flat=True)),
            ['A', 'Z'],
        )

    def test_api_returns_projects_in_order_sequence(self):
        import json
        make_project('Third', order=3)
        make_project('First', order=1)
        make_project('Second', order=2)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual([p['title'] for p in data], ['First', 'Second', 'Third'])


class SkillQuerysetOrderingTests(TestCase):

    def test_skills_ordered_by_category_then_order_then_name(self):
        make_skill('OOP', Skill.CONCEPTS, order=1)
        make_skill('Python', Skill.LANGUAGES, order=1)
        make_skill('Go', Skill.LANGUAGES, order=2)
        # 'Concepts' < 'Languages' alphabetically, so Concepts appears first.
        result = list(Skill.objects.values_list('category', 'name'))
        self.assertEqual(result[0], (Skill.CONCEPTS, 'OOP'))
        self.assertEqual(result[1], (Skill.LANGUAGES, 'Python'))
        self.assertEqual(result[2], (Skill.LANGUAGES, 'Go'))

    def test_api_returns_skills_grouped_preserving_order(self):
        import json
        make_skill('Go', Skill.LANGUAGES, order=2)
        make_skill('Python', Skill.LANGUAGES, order=1)
        response = self.client.get('/api/skills/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # Python has order=1, Go has order=2 — Python must come first.
        self.assertEqual(data[Skill.LANGUAGES], ['Python', 'Go'])


# ── Class 5: admin configuration / mixin structural tests ─────────────────────

class AdminMixinConfigurationTests(TestCase):

    def setUp(self):
        self.site = AdminSite()

    def test_project_admin_inherits_sortable_mixin(self):
        self.assertTrue(issubclass(ProjectAdmin, SortableAdminMixin))

    def test_skill_admin_inherits_sortable_mixin(self):
        self.assertTrue(issubclass(SkillAdmin, SortableAdminMixin))

    def test_project_admin_sort_key_is_order(self):
        instance = ProjectAdmin(Project, self.site)
        self.assertEqual(instance.default_order_field, 'order')

    def test_skill_admin_sort_key_is_order(self):
        instance = SkillAdmin(Skill, self.site)
        self.assertEqual(instance.default_order_field, 'order')

    def test_project_admin_ordering_starts_with_order(self):
        self.assertEqual(ProjectAdmin.ordering[0], 'order')

    def test_skill_admin_ordering_starts_with_order(self):
        self.assertEqual(SkillAdmin.ordering[0], 'order')

    def test_project_admin_title_in_list_display_links(self):
        self.assertIn('title', ProjectAdmin.list_display_links)

    def test_skill_admin_name_in_list_display_links(self):
        self.assertIn('name', SkillAdmin.list_display_links)

    def test_skill_admin_overrides_get_max_order(self):
        self.assertIn('get_max_order', SkillAdmin.__dict__)

    def test_project_admin_does_not_override_get_max_order(self):
        self.assertNotIn('get_max_order', ProjectAdmin.__dict__)


# ── Class 6: homepage template structure ──────────────────────────────────────

class HomepageTemplateTests(TestCase):

    def setUp(self):
        self.response = self.client.get('/')
        self.html = self.response.content.decode()

    def test_homepage_returns_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_scroll_top_component_is_defined(self):
        self.assertIn('const ScrollTop', self.html)

    def test_scroll_top_uses_anchor_href_home(self):
        self.assertIn('href="#home"', self.html)

    def test_scroll_top_visibility_controlled_by_state(self):
        self.assertIn('if (!visible) return null', self.html)

    def test_scroll_top_has_high_zindex(self):
        self.assertIn('zIndex: 9999', self.html)

    def test_scroll_top_is_rendered_in_app(self):
        self.assertIn('<ScrollTop />', self.html)

    def test_publications_section_present(self):
        self.assertIn('id="publications"', self.html)

    def test_navbar_includes_publications_link(self):
        self.assertIn("'Publications'", self.html)

    def test_publications_api_fetch_in_app(self):
        self.assertIn('/api/publications/', self.html)


# ── Class 7: publications API and model ───────────────────────────────────────

class PublicationsAPITests(TestCase):

    def setUp(self):
        Publication.objects.all().delete()  # remove seed-migration data
        self.pub = Publication.objects.create(
            title='Test Publication',
            role='Test Author',
            journal='Test Journal',
            metrics='Impact Factor: 1.0 | CiteScore: 2.0',
            year=2024,
            description=['Bullet one.', 'Bullet two.'],
            link='https://doi.org/10.0000/test',
            order=1,
        )

    def test_api_returns_200(self):
        self.assertEqual(self.client.get('/api/publications/').status_code, 200)

    def test_api_returns_json_list(self):
        import json
        data = json.loads(self.client.get('/api/publications/').content)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_api_includes_required_fields(self):
        import json
        pub = json.loads(self.client.get('/api/publications/').content)[0]
        for field in ('title', 'role', 'journal', 'metrics', 'year', 'description', 'link'):
            self.assertIn(field, pub, f'field "{field}" missing from API response')

    def test_api_description_is_list(self):
        import json
        pub = json.loads(self.client.get('/api/publications/').content)[0]
        self.assertIsInstance(pub['description'], list)
        self.assertEqual(len(pub['description']), 2)

    def test_api_respects_order_field(self):
        import json
        Publication.objects.create(
            title='Earlier Pub', role='r', journal='j', year=2023,
            description=[], order=2,
        )
        data = json.loads(self.client.get('/api/publications/').content)
        self.assertEqual(data[0]['title'], 'Test Publication')
        self.assertEqual(data[1]['title'], 'Earlier Pub')

    def test_model_str_returns_title(self):
        self.assertEqual(str(self.pub), 'Test Publication')

    def test_model_default_ordering_by_order_then_year(self):
        pub2 = Publication.objects.create(
            title='Second', role='r', journal='j', year=2023,
            description=[], order=2,
        )
        titles = list(Publication.objects.values_list('title', flat=True))
        self.assertEqual(titles[0], 'Test Publication')
        self.assertEqual(titles[1], 'Second')

    def test_publication_admin_inherits_sortable_mixin(self):
        self.assertTrue(issubclass(PublicationAdmin, SortableAdminMixin))

    def test_publication_admin_ordering_starts_with_order(self):
        self.assertEqual(PublicationAdmin.ordering[0], 'order')
