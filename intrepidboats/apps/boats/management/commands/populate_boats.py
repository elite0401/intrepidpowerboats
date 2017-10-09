from os.path import join, basename

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from environ import environ

from intrepidboats.apps.boats.models import BoatModelGroup, Motor, MotorSelection, OptionalEquipment, TOP_FEATURE, \
    ANCHOR_FEATURE, SS_RUB_RAIL_INSERT_FEATURE, DIVE_DOOR_FEATURE, DeckPlan, BoatGeneralFeature, AboutTheBoat, \
    AboutTheBoatImage, Video


class Command(BaseCommand):
    help = 'Create boats and boat groups'

    objects = {
        "Center Console": {
            "image": "boat-01.jpg",
            "boats": {
                "475 Panacea": {
                    "standard_fuel": "569 Gallons",
                    "beam": "13' 8\"",
                    "length": "47' 6\"",
                    "water": "130 Gallons",
                },
                "400 Center Console": {
                    "standard_fuel": "307 Gallons",
                    "beam": "11' 1\"",
                    "length": "40' 3\"",
                    "water": "40 Gallons",
                },
                "245 Center Console": {
                    "standard_fuel": "147 Gallons",
                    "beam": "8' 6\"",
                    "length": "25' 3\"",
                    "water": "16 Gallons"
                },
                "300 Center Console": {
                    "standard_fuel": "173 Gallons",
                    "beam": "9' 6\"",
                    "length": "30' 0\"",
                    "water": "30 Gallons",
                },
                "327 Center Console": {
                    "standard_fuel": "221 Gallons",
                    "beam": "9 ' 6\"",
                    "length": "32' 7\"",
                    "water": "20 Gallons",
                },
                "327 CC Tournament Edition": {
                    "standard_fuel": "221 Gallons",
                    "beam": "9' 6\"",
                    "length": "32' 7\"",
                    "water": "20 Gallons",

                },
                "375 Center Console": {
                    "standard_fuel": "300 Gallons",
                    "beam": "10' 6\"",
                    "length": "37' 9\"",
                    "water": "40 Gallons",
                },
                "410 Evolution": {
                    "standard_fuel": "449 gallons",
                    "beam": "12.60 feet",
                    "length": "41’ 2\"",
                    "water": "80 gallons",
                },
            }
        },
        "Cuddy ": {
            "image": "boat-02.jpg",
            "boats": {

                "327 Cuddy": {
                    "standard_fuel": "237 Gallons",
                    "beam": "9' 6\"",
                    "length": "32' 7\"",
                    "water": "20 Gallons"
                },
                "407 Cuddy": {
                    "standard_fuel": "387 Gallons",
                    "beam": "11' 1\"",
                    "length": "40' 0\"",
                    "water": "50 Gallons",
                },
            }
        },
        "Walkaround": {
            "image": "boat-03.jpg",
            "boats": {

                "375 Walkaround": {
                    "standard_fuel": "394 Gallons",
                    "beam": "11' 0\"",
                    "length": "37' 5\"",
                    "water": "50 Gallons",
                },
            }
        },
        "Sport Yacht": {
            "image": "boat-04.jpg",
            "boats": {

                "430 Sport Yacht": {
                    "standard_fuel": "376 Gallons",
                    "beam": "12' 8\"",
                    "length": "43' 0\"",
                    "water": "100 Gallons",
                },
                "475 Sport Yacht": {
                    "standard_fuel": "483 Gallons",
                    "beam": "13' 8\"",
                    "length": "47' 6\"",
                    "water": "100 Gallons",
                },
                "390 Sport Yacht": {
                    "standard_fuel": "396 Gallons",
                    "beam": "12' 0\"",
                    "length": "39' 8\"",
                    "water": "60 Gallons",
                },
            }
        },
    }

    images = {
        "base": "backgroundimage.png",
        "hull": "hull.png",
        "boot_stripe": "bootstripe.png",
        "boot_stripe_accent": "bootstripeaccent.png",
        "sheer_stripe": "sheerstripe.png",
        "sheer_stripe_accent": "sheerstripeaccent.png",
        "thumbnail": "thumbnail.jpg",
        "logo": "logo.png",
    }

    motors = {
        "yamaha": {
            "image": "img-motor-yamaha.jpg"
        },
        "7-marine": {
            "image": "img-motor-seven-marine.jpg"
        },
        "mercury": {
            "image": "img-motor-mercury.jpg"
        },
    }

    motor_selection = {
        "yamaha": {
            "grey": {
                "image": "yamahagrey.png",
            },
            "white": {
                "image": "yamahawhite.png",
            },
        },
        "mercury": {
            "white": {
                "image": "mercurywhite.png"
            },
            "black": {
                "image": "mercuryblack.png"
            },
        },
        "7-marine": {
            "grey": {
                "image": "7marinegrey.png"
            },
            "grey with cowl": {
                "image": "7marinegreywithcowl.png"
            },
            "white": {
                "image": "7marinewhite.png"
            },
            "white with cowl": {
                "image": "7marinewhitewithcowl.png"
            }
        }
    }

    features = {
        "Tower": {
            "image": "tower.png",
            "kind": TOP_FEATURE,
        },
        "Anchor": {
            "image": "anchor.png",
            "kind": ANCHOR_FEATURE
        },
        "ss rub rail insert": {
            "image": "Intrepid245SSInsert.png",
            "kind": SS_RUB_RAIL_INSERT_FEATURE
        },
        "dive door": {
            "image": "divedoor.png",
            "kind": DIVE_DOOR_FEATURE,
        },
    }

    optional_equipment = {
        "This one has a video!": {
            "vimeo": "61266245",
        },
        "Bow Eye": {
            "image": "Bow_eye.jpg",
        },
        "Integral Motor Bracket": {
            "image": "Integral-Motor-Bracket.jpg",
        },
        "PVC Foam Core Vacuum-bagged Non-woven Multi-directional and Uni-directional Fibers all Hand Laid": {
            "image": "pvc-formcore-vac.jpg",
        },
        "Heavy Duty Vinyl Rubrail": {
            "image": "rubrail.jpg",
        },
        "Console Windshield": {
            "image": "windshield.jpg",
        },
        "No preview here": {
        },
    }

    feature_lists = {
        "Important features":
            '''<ul class="list bulleted">
                <li>Compact diesel generator</li>
                <li>Aluminum fuel tanks with level senders</li>
                <li>Bronze thru-hulls with seacocks below waterline</li></li>
                <li>Fire suppression system in mechanical room w/automatic generator</li>
                <li>Gas/water separator on generator exhaust system</li>
                <li>Power assisted hydraulic steering w/tilt helm</li>
                <li>Waste/holding tank odor proof polyethylene w/level sender</li>
                <li>Water tank food grade polyethylene</li>
               </ul>''',
        "Intrepid features":
            '''<ul class="list bulleted">
                <li>Bridge deck Infinity flooring woven vinyl</li>
                <li>Compass</li>
                <li>Electronics console, at helm</li>
                <li>Electronics console, companion port side</li>
                <li>Helm Seat double, three way electronic control and adjustable bolster</li>
                <li>Lighting, hardtop, 12 volt, LED</li>
                <li>Lighting, Red overhead night lighting</li>
                <li>Outlets, 1 x 2 gang GFCI</li>
                <li>Outlets, 2 x USB at helm console</li>
                <li>Settee L shaped (port side) with custom adjustable co-pilot seat fwd</li>
                <li>Settee, L shaped (starboard)</li>
                <li>Steering wheel, stainless steel</li>
                <li>Sunroof (electric)</li>
               </ul>''',
        "Incredible features":
            '''<ul class="list bulleted">
                <li>Blinds</li>
                <li>Electric Head w/fresh water supply</li>
                <li>Exhaust fan</li>
                <li>Faucet single lever</li>
                <li>Outlets, AC 1 double outlets ELCI protected</li>
                <li>Shower stall with acrylic door</li>
                <li>Skylights (1) fixed</li>
                <li>Sole tile and fiberglass finish</li>
                <li>Toilet Paper holder behind locker door</li>
               </ul>''',
    }

    about_galleries = {
        'interior': [
            '001.jpg', '003.jpg', '005.jpg', '006.jpg', 'mod-401-00.jpg',
            'img-int-diff-01.png', 'bg-intrepid-difference-02.jpg',
        ],
        'exterior': [
            '000.jpg', '001.jpg', '004.jpg', '005.jpg', '008.jpg', '009.jpg',
            '010.jpg', '011.jpg', '012.jpg', '013.jpg', '014.jpg', '015.jpg',
            '016.jpg', '017.jpg', '018.jpg', '019.jpg', '020.jpg', '021.jpg',
        ]
    }

    vimeo_codes = [
        '65926737',
        '102530775',
        '45932563',
        '142830093',
        '134367155',
        '59322299',
        '114480315',
        '200836255',
    ]

    def handle(self, *args, **options):
        lib_path = environ.Path(__file__) - 1
        files_path = join(str(lib_path), "images", "groups")
        motors = self.create_motors()
        for group_name, attrs in self.objects.items():
            image_page = join(files_path, attrs["image"], )
            boats = attrs.get("boats", {})
            with open(image_page, "rb") as an_image:
                self.create_group(group_name, ContentFile(an_image.read(), basename(image_page)), boats, motors)

    def create_motors(self):
        motors = []
        lib_path = environ.Path(__file__) - 1
        files_path = join(str(lib_path), "images", "motors")
        for key, attrs in self.motors.items():
            image_page = join(files_path, attrs["image"], )
            with open(image_page, "rb") as an_image:
                motor, _ = Motor.objects.get_or_create(
                    title=key,
                    image=ContentFile(an_image.read(), basename(image_page))
                )
                motors.append(motor)
        return motors

    def create_group(self, name, image, boats, motors):
        group, created = BoatModelGroup.objects.get_or_create(
            title=name,
            defaults={
                "show_image": image,
            }
        )
        if created:
            self.populate_boats(group, boats, motors)

    def populate_boats(self, group, boats, motors):
        for boat, attrs in boats.items():
            attrs = self.get_boat_attrs(attrs)
            boat_model = group.boats.create(
                title=boat,
                **attrs
            )
            self.create_motor_selections(boat_model, motors)
            self.create_features(boat_model)
            self.create_optional_equipment(boat_model)
            self.create_deck_plan(boat_model)
            self.create_feature_lists(boat_model)
            self.create_about_data(boat_model)
            self.create_videos(boat_model)

    def get_boat_attrs(self, attrs):
        default = {}
        for key, value in self.images.items():
            default[key] = self.get_image(value)
        return {**default, **attrs}

    def get_image(self, value):
        lib_path = environ.Path(__file__) - 1
        files_path = join(str(lib_path), "images", "groups", "boats", value)
        content = None
        with open(files_path, "rb") as an_image:
            content = ContentFile(an_image.read(), basename(files_path))
        return content

    def create_motor_selections(self, boat, motors):
        for motor in motors:
            selection_model = MotorSelection.objects.create(motor=motor, boat=boat)
            selections = self.motor_selection.get(motor.title, {})
            for selection_name, attrs in selections.items():
                lib_path = environ.Path(__file__) - 1
                files_path = join(str(lib_path), "images", "groups", "boats", "motors", attrs["image"])
                with open(files_path, "rb") as an_image:
                    content = ContentFile(an_image.read(), basename(files_path))
                    selection_model.options.create(title=selection_name, image=content)

    def create_features(self, boat_model):
        for name, attrs in self.features.items():
            lib_path = environ.Path(__file__) - 1
            file_path = join(str(lib_path), "images", "groups", "boats", "features", attrs["image"])
            empty_path = join(str(lib_path), "images", "groups", "boats", "features", "empty.png")

            with open(empty_path, "rb") as empty_image:
                empty_content = ContentFile(empty_image.read(), basename(empty_path))
                with open(file_path, "rb") as an_image:
                    content = ContentFile(an_image.read(), basename(file_path))

                    feature = boat_model.features.create(title=name, kind=attrs["kind"], available=True)
                    feature.options.create(image=content, title="Yes", display_value=feature.title)
                    feature.options.create(image=empty_content, title="No", default=True)

    def create_optional_equipment(self, boat_model):
        lib_path = environ.Path(__file__) - 1
        files_path = join(str(lib_path), "images", "optional_equipment")
        for name, attrs in self.optional_equipment.items():
            if 'image' in attrs:
                image_page = join(files_path, attrs["image"], )
                with open(image_page, "rb") as an_image:
                    OptionalEquipment.objects.create(
                        description=name,
                        boat_model=boat_model,
                        thumbnail=ContentFile(an_image.read(), basename(image_page)),
                    )
            elif 'vimeo' in attrs:
                OptionalEquipment.objects.create(
                    description=name,
                    boat_model=boat_model,
                    vimeo_id=attrs['vimeo'],
                )
            else:
                OptionalEquipment.objects.create(
                    description=name,
                    boat_model=boat_model,
                )

    def create_deck_plan(self, boat_model):
        lib_path = environ.Path(__file__) - 1
        files_path = join(str(lib_path), "images", "deck_plan")
        image_page = join(files_path, "img-model-deck.jpg", )
        with open(image_page, "rb") as an_image:
            DeckPlan.objects.create(
                image=ContentFile(an_image.read(), basename(image_page)),
                boat=boat_model,
            )

    def create_feature_lists(self, boat_model):
        for _ in range(2):
            for title, _ in self.feature_lists.items():
                BoatGeneralFeature.objects.create(
                    title=title,
                    boat=boat_model,
                )

    def create_about_data(self, boat):
        description = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ne in odium veniam, si amicum
        destitero tueri. Commoda autem et incommoda in eo genere sunt Lorem ipsum dolor sit amet, consectetur
        adipiscing elit. Ne in odium veniam, si amicum destitero tueri. Commoda autem et incommoda in eo gener

        Sunt Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ne in odium veniam, si amicum destitero
        tueri. Commoda autem et incommoda in eo genere sunte sunt

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ne in odium veniam, si amicum"""

        lib_path = environ.Path(__file__) - 1
        brochure_path = join(str(lib_path), "files", "a_brochure.pdf")
        with open(brochure_path, "rb") as a_file:
            about_the_boat = AboutTheBoat.objects.create(
                title='Lorem ipsum dolor sit amet, consectetur',
                description=description,
                brochure=ContentFile(a_file.read(), basename(brochure_path)),
                boat=boat,
            )

        self.create_about_galleries(about_the_boat)

    def create_about_galleries(self, about_the_boat):
        lib_path = environ.Path(__file__) - 1
        files_path = join(str(lib_path), "images", "about")
        for kind, images in self.about_galleries.items():
            for image_name in images:
                image_path = join(files_path, kind, image_name)
                with open(image_path, "rb") as an_image:
                    AboutTheBoatImage.objects.create(
                        image=ContentFile(an_image.read(), basename(image_path)),
                        kind=kind.upper(),
                        about_the_boat=about_the_boat,
                    )

    def create_videos(self, boat):
        for code in self.vimeo_codes:
            Video.objects.create(vimeo_video_code=code, boat=boat)
