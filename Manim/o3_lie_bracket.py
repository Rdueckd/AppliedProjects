r"""An annotated Manim Community Edition demo of O(3), SO(3), and the Lie bracket.

WHAT THIS FILE IS
-----------------
This is a Python SCRIPT for Manim Community Edition (the package named `manim`).
It is NOT written for 3Blue1Brown's separate `manimgl` package; those versions
have different APIs. Manim reads the Scene below and renders it to a video.

ONE-TIME SETUP
--------------
1. Install Python, then open a terminal in a folder for this project.
   Optional but recommended: isolate Manim in a Python virtual environment.

   macOS / Linux:
       python3 -m venv .venv
       source .venv/bin/activate

   Windows (PowerShell):
       py -m venv .venv
       .venv\Scripts\Activate.ps1

   If PowerShell blocks activation, see Microsoft's execution-policy guidance,
   or use the virtual environment's Python executable directly instead.

2. With that environment active, install Manim Community Edition:

       python -m pip install manim

3. Install a LaTeX distribution because this particular scene uses MathTex to
   draw equations. Common options are MiKTeX (Windows), MacTeX (macOS), and
   TeX Live (Linux). A working LaTeX installation usually also needs dvisvgm.
   Some operating systems may also require system packages for Cairo/Pango;
   consult the official Manim installation guide if pip reports an error.
   If video encoding fails, check that FFmpeg is available for your setup.

   Official instructions: https://docs.manim.community/en/stable/installation.html

4. Save this file as `o3_lie_bracket.py` and run the following command from the
   SAME directory (with the environment active):

       python -m manim -pql o3_lie_bracket.py O3LieBracket

   Command explained:
       python -m manim  Run the installed Manim Python module.
       -p               Play/open the resulting video when rendering finishes.
       -ql              Render at low quality for faster iteration.
       o3_lie_bracket.py  The input Python script.
       O3LieBracket     The Scene CLASS name to render (defined below).

   For a higher-quality render, change -ql to -qh:

       python -m manim -pqh o3_lie_bracket.py O3LieBracket

   Manim normally saves the output under a `media/` directory. If your setup
   cannot automatically open videos, omit -p and open the generated MP4 there.

QUICK CUSTOMIZATIONS
--------------------
* Change `theta` to make the two large rotations bigger/smaller.
* Change `eps` to vary the small commutator-loop rotations. Smaller values
  better approximate the Lie bracket but are harder to see in a video.
* Change `run_time` to speed up or slow down an animation.
* Change `self.wait(...)` to adjust pauses between segments.
* Change `phi`, `theta` (in the camera settings), and `zoom` for a new view.

MATH ROAD MAP
-------------
O(3)  = orthogonal 3x3 real matrices: Q^T Q = I, determinant +/- 1.
SO(3) = those orthogonal matrices with determinant +1 (proper rotations).
so(3) = skew-symmetric 3x3 matrices: A^T = -A (the Lie algebra of SO(3)).

With conventional generators of rotations about x, y, and z,

    [J_x, J_y] = J_x J_y - J_y J_x = J_z.

Near the identity, the group commutator obeys

    R_x(e) R_y(e) R_x(-e) R_y(-e) = R_z(e^2) + O(e^3).

This is an approximation for small e, not an exact equality for finite e.
"""

# NumPy supplies arrays and linear algebra utilities; here we use np.diag(...)
# to construct a reflection matrix. The import name `np` is a common shorthand.
import numpy as np

# Manim provides Cube, Dot3D, ThreeDAxes, MathTex, FadeIn, Rotate, colors,
# directions (RIGHT, UP), angles (DEGREES), and the ThreeDScene base class.
# `import *` is conventional in small Manim scenes, though usually avoided in
# larger Python projects because it imports many names into the current scope.
from manim import *


# Every renderable Manim animation is a Scene. ThreeDScene is a Scene with
# 3D-camera functionality. The CLI looks for a class with the name given above.
class O3LieBracket(ThreeDScene):
    # Manim calls construct() to build the animation; you do not call it yourself.
    # `self` is this scene, so self.play(...) animates objects in this scene.
    def construct(self):
        # CAMERA: phi is the angle from the positive z-axis; theta is the
        # azimuth around the z-axis. Both are expressed in radians, so Manim's
        # DEGREES constant converts human-readable degrees to radians.
        # This camera setting affects ONLY what we see, not the rotation axes.
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.85,
        )

        # A coordinate system makes it clear which direction is +x, +y, +z.
        # x_range=[min, max, step] configures the axis's numerical labels/ticks;
        # x_length controls its physical length in Manim's scene units.
        axes = ThreeDAxes(
            x_range=[-2.2, 2.2, 1],
            y_range=[-2.2, 2.2, 1],
            z_range=[-2.2, 2.2, 1],
            x_length=4.4,
            y_length=4.4,
            z_length=4.4,
        )

        # VGroup groups objects so one Rotate(...) can rotate BOTH the cube
        # and the yellow marker together. The cube alone is symmetric enough
        # that it can be hard to distinguish rotation/reflection visually.
        solid = VGroup(
            Cube(
                side_length=1.6,   # Length of each cube edge in scene units.
                fill_color=BLUE,    # Color of the faces.
                fill_opacity=0.17,  # 0 = transparent; 1 = opaque.
                stroke_color=BLUE_B,  # Color of edges/outlines.
                stroke_width=2,    # Edge line width.
            ),
            # One special corner: the marker moves when the cube transforms.
            # The point is (x, y, z); radius is the marker's 3D size.
            Dot3D(point=[0.8, 0.8, 0.8], radius=0.14, color=YELLOW),
        )
        # Store this object's original position and orientation. Later,
        # Restore(solid) animates it back without us tracking rotation angles.
        solid.save_state()

        # MathTex renders LaTeX mathematical notation (requires LaTeX installed).
        # r"..." is a raw Python string, so LaTeX backslashes need no escaping.
        # to_edge(UP/DOWN) pins the equation near the corresponding screen edge.
        heading = MathTex(
            r"O(3)=\{Q\in\mathbb{R}^{3\times 3}:Q^TQ=I\}",
            font_size=39,
        ).to_edge(UP)
        caption = MathTex(r"\det Q=+1\ \text{or}\ -1", font_size=34).to_edge(DOWN)

        # Text in a ThreeDScene would otherwise live in 3D space and be
        # projected by the camera. This keeps labels fixed on the 2D screen.
        self.add_fixed_in_frame_mobjects(heading, caption)

        # self.play() runs animations, optionally in parallel. Create draws
        # the axes; FadeIn makes the cube/marker appear. run_time is in seconds.
        self.play(Create(axes), FadeIn(solid), run_time=1.5)
        self.wait(0.5)  # Hold the frame for half a second.

        # ---------------------------------------------------------------
        # SECTION 1: A REFLECTION IN O(3), BUT NOT IN SO(3)
        # ---------------------------------------------------------------
        # diag(-1, 1, 1) flips x while leaving y and z unchanged. Its
        # determinant is -1, so this transformation is an element of O(3),
        # but it is not a proper 3D rotation (not an element of SO(3)).
        # `copy()` is important: we want to keep the original cube intact.
        # `apply_matrix` transforms the copied object's point coordinates.
        mirror = solid.copy().apply_matrix(np.diag([-1.0, 1.0, 1.0]))

        # Transform(old, new) morphs an existing label into the new expression;
        # this is cleaner than removing and recreating each label manually.
        # FadeOut/FadeIn swap the two orientations on screen. We do not try
        # to continuously deform an orthogonal rotation into a reflection:
        # those belong to different connected components of O(3).
        self.play(
            Transform(
                caption,
                MathTex(r"\det Q=-1:\quad x\mapsto -x", font_size=34).to_edge(DOWN),
            ),
            FadeOut(solid),
            FadeIn(mirror),
            run_time=1.3,
        )
        self.wait(0.5)
        self.play(
            FadeOut(mirror),
            FadeIn(solid),
            Transform(
                caption,
                MathTex(r"SO(3):\quad \det Q=+1", font_size=34).to_edge(DOWN),
            ),
        )

        # ---------------------------------------------------------------
        # SECTION 2: ROTATIONS ABOUT DIFFERENT AXES DO NOT COMMUTE
        # ---------------------------------------------------------------
        theta = 70 * DEGREES   # A visible 70-degree rotation, in radians.

        # RIGHT is Manim's unit x-direction [1, 0, 0].
        # UP is Manim's unit y-direction [0, 1, 0].
        # ORIGIN = [0, 0, 0], our chosen center of rotation.
        # In R_y(theta)R_x(theta), the RIGHTMOST matrix acts FIRST on points.
        self.play(Transform(
            caption,
            MathTex(r"R_y(\theta)R_x(\theta)", font_size=36).to_edge(DOWN),
        ))
        self.play(
            Rotate(solid, angle=theta, axis=RIGHT, about_point=ORIGIN),
            run_time=1,
        )  # First: rotate around the fixed, global x-axis.
        self.play(
            Rotate(solid, angle=theta, axis=UP, about_point=ORIGIN),
            run_time=1,
        )  # Second: rotate around the fixed, global y-axis.

        # solid[0] is the Cube; solid[1] is the yellow Dot3D.
        # get_center() reads its *current* position after both rotations.
        # We leave an orange dot at this endpoint so we can compare the result.
        end_xy = Dot3D(point=solid[1].get_center(), radius=0.12, color=ORANGE)
        self.add(end_xy)      # add(...) shows an object immediately, no animation.
        self.play(Restore(solid), run_time=0.7)

        # Now reverse the order, starting again from the INITIAL position.
        # The product is R_x(theta)R_y(theta), with R_y acting first.
        self.play(Transform(
            caption,
            MathTex(r"R_x(\theta)R_y(\theta)", font_size=36).to_edge(DOWN),
        ))
        self.play(Rotate(solid, angle=theta, axis=UP, about_point=ORIGIN), run_time=1)
        self.play(Rotate(solid, angle=theta, axis=RIGHT, about_point=ORIGIN), run_time=1)

        # The green dot marks the endpoint after the opposite ordering.
        # The two differently colored endpoints reveal noncommutativity.
        end_yx = Dot3D(point=solid[1].get_center(), radius=0.12, color=GREEN)
        self.add(end_yx)
        self.play(Transform(
            caption,
            MathTex(r"R_yR_x\ne R_xR_y", font_size=38).to_edge(DOWN),
        ))
        self.wait(1)

        # Clean up the comparison dots, put the cube back at the start, and
        # change the formulas to describe the Lie algebra rather than the group.
        self.play(FadeOut(end_xy), FadeOut(end_yx), Restore(solid), run_time=0.8)
        self.play(
            Transform(
                heading,
                MathTex(r"\mathfrak{so}(3)=\{A:A^T=-A\}", font_size=40).to_edge(UP),
            ),
            Transform(
                caption,
                MathTex(r"[J_x,J_y]=J_xJ_y-J_yJ_x=J_z", font_size=38).to_edge(DOWN),
            ),
        )
        self.wait(0.6)

        # ---------------------------------------------------------------
        # SECTION 3: THE LIE BRACKET AS A SMALL ROTATION LOOP
        # ---------------------------------------------------------------
        # J_x, J_y and J_z are infinitesimal rotation generators (3x3
        # skew-symmetric matrices). Their Lie bracket is the matrix
        # commutator [A, B] = AB - BA, not the same as a vector cross product
        # (although so(3) has a close relationship with the cross product).
        #
        # The group commutator is a LOOP of four finite rotations:
        #   R_x(e) R_y(e) R_x(-e) R_y(-e).
        # Applying this product to column vectors happens RIGHT TO LEFT:
        #   1) R_y(-e)   2) R_x(-e)   3) R_y(e)   4) R_x(e).
        # The first-order changes cancel, leaving (to leading order) an
        # e^2-sized rotation around z, encoding [J_x, J_y] = J_z.
        eps = 0.55  # RADIANS (~32 degrees). Reduce for a more exact approximation.

        self.play(Transform(
            caption,
            MathTex(
                r"R_x(\varepsilon)R_y(\varepsilon)R_x(-\varepsilon)R_y(-\varepsilon)"
                r"\approx R_z(\varepsilon^2)",
                font_size=28,  # Smaller font so this longer formula fits.
            ).to_edge(DOWN),
        ))

        # Each (axis, angle) pair is unpacked by the for loop. Each play()
        # is sequential, so we get four distinct animations rather than four
        # simultaneous rotations. axis=UP means y; axis=RIGHT means x.
        for axis, angle in [
            (UP, -eps),
            (RIGHT, -eps),
            (UP, eps),
            (RIGHT, eps),
        ]:
            self.play(
                Rotate(solid, angle=angle, axis=axis, about_point=ORIGIN),
                run_time=0.6,
            )

        # End with the algebraic result, held on screen for two seconds.
        # \boxed is standard LaTeX and requires MathTex's LaTeX dependency.
        self.play(Transform(
            caption,
            MathTex(r"\boxed{[J_x,J_y]=J_z}", font_size=42).to_edge(DOWN),
        ))
        self.wait(2)


# There is deliberately NO `O3LieBracket().construct()` call below.
# Manim's CLI discovers the Scene class and runs it as part of rendering.
