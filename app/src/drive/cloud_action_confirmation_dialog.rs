use warpui::elements::{Container, CornerRadius, Dismiss, MouseStateHandle, Radius};
use warpui::fonts::Weight;
use warpui::platform::Cursor;
use warpui::ui_components::button::ButtonVariant;
use warpui::ui_components::components::{Coords, UiComponent, UiComponentStyles};
use warpui::{AppContext, Element, Entity, SingletonEntity, TypedActionView, View, ViewContext};

use crate::appearance::Appearance;
use crate::ui_components::blended_colors;
use crate::ui_components::dialog::{dialog_styles, Dialog};

const BUTTON_PADDING: f32 = 12.;
const BUTTON_FONT_SIZE: f32 = 14.;
const BUTTON_BORDER_RADIUS: f32 = 4.;
const BORDER_WIDTH: f32 = 1.;

const DIALOG_WIDTH: f32 = 450.;
const CANCEL_TEXT: &str = "取消";

const DELETE_TEAM_TITLE_TEXT: &str = "确定要删除此团队吗？";
const LEAVE_TEAM_TITLE_TEXT: &str = "确定要离开此团队吗？";
const REMOVE_TEAM_MEMBER_TITLE_TEXT: &str = "确定要移除此成员吗？";

const DELETE_TEAM_BODY_TEXT: &str =
    "删除此团队会永久删除团队及其所有相关内容，包括账单信息或额度。你将无法恢复它们。";
const LEAVE_TEAM_BODY_TEXT: &str = "如需重新加入，你需要再次被邀请。";
const LEAVE_TEAM_RELOAD_CREDITS_BODY_TEXT: &str = "如果离开此团队，你将无法访问与其关联的剩余 Reload 额度。如果之后重新加入同一团队，你将重新获得未使用且未过期额度的访问权限。";
const REMOVE_TEAM_MEMBER_RELOAD_CREDITS_BODY_TEXT: &str = "此成员将无法访问与此团队关联的剩余 Reload 额度。如果之后重新加入，他们将重新获得未使用且未过期额度的访问权限。";

const DELETE_TEAM_CONFIRM_TEXT: &str = "确认删除";
const LEAVE_TEAM_CONFIRM_TEXT: &str = "确认离开";
const LEAVE_TEAM_RELOAD_CREDITS_CONFIRM_TEXT: &str = "离开团队";
const REMOVE_TEAM_MEMBER_RELOAD_CREDITS_CONFIRM_TEXT: &str = "移除成员";

pub enum CloudActionConfirmationDialogEvent {
    Cancel,
    Confirm,
}

#[derive(Debug)]
pub enum CloudActionConfirmationDialogAction {
    Cancel,
    Confirm,
}

#[derive(Default)]
pub enum CloudActionConfirmationDialogVariant {
    LeaveTeam,
    DeleteTeam,
    LeaveTeamReloadCredits,
    RemoveTeamMemberReloadCredits,
    #[default]
    None,
}

pub struct CloudActionConfirmationDialog {
    cancel_mouse_state: MouseStateHandle,
    confirm_mouse_state: MouseStateHandle,
    variant: CloudActionConfirmationDialogVariant,
    confirmation_button_enabled: bool,
}

impl CloudActionConfirmationDialog {
    pub fn new() -> Self {
        Self {
            cancel_mouse_state: Default::default(),
            confirm_mouse_state: Default::default(),
            variant: Default::default(),
            confirmation_button_enabled: true,
        }
    }

    pub fn set_variant(&mut self, variant: CloudActionConfirmationDialogVariant) {
        self.variant = variant;
    }

    pub fn set_confirmation_button_enabled(&mut self, enabled: bool) {
        self.confirmation_button_enabled = enabled;
    }

    fn title_text(&self) -> String {
        match self.variant {
            CloudActionConfirmationDialogVariant::LeaveTeam
            | CloudActionConfirmationDialogVariant::LeaveTeamReloadCredits => {
                LEAVE_TEAM_TITLE_TEXT.to_string()
            }
            CloudActionConfirmationDialogVariant::DeleteTeam => DELETE_TEAM_TITLE_TEXT.to_string(),
            CloudActionConfirmationDialogVariant::RemoveTeamMemberReloadCredits => {
                REMOVE_TEAM_MEMBER_TITLE_TEXT.to_string()
            }
            CloudActionConfirmationDialogVariant::None => String::new(),
        }
    }

    fn body_text(&self) -> String {
        match self.variant {
            CloudActionConfirmationDialogVariant::LeaveTeam => LEAVE_TEAM_BODY_TEXT.to_string(),
            CloudActionConfirmationDialogVariant::DeleteTeam => DELETE_TEAM_BODY_TEXT.to_string(),
            CloudActionConfirmationDialogVariant::LeaveTeamReloadCredits => {
                LEAVE_TEAM_RELOAD_CREDITS_BODY_TEXT.to_string()
            }
            CloudActionConfirmationDialogVariant::RemoveTeamMemberReloadCredits => {
                REMOVE_TEAM_MEMBER_RELOAD_CREDITS_BODY_TEXT.to_string()
            }
            CloudActionConfirmationDialogVariant::None => String::new(),
        }
    }

    fn confirm_button_text(&self) -> String {
        match self.variant {
            CloudActionConfirmationDialogVariant::LeaveTeam => LEAVE_TEAM_CONFIRM_TEXT.to_string(),
            CloudActionConfirmationDialogVariant::DeleteTeam => {
                DELETE_TEAM_CONFIRM_TEXT.to_string()
            }
            CloudActionConfirmationDialogVariant::LeaveTeamReloadCredits => {
                LEAVE_TEAM_RELOAD_CREDITS_CONFIRM_TEXT.to_string()
            }
            CloudActionConfirmationDialogVariant::RemoveTeamMemberReloadCredits => {
                REMOVE_TEAM_MEMBER_RELOAD_CREDITS_CONFIRM_TEXT.to_string()
            }
            CloudActionConfirmationDialogVariant::None => String::new(),
        }
    }
}

impl Entity for CloudActionConfirmationDialog {
    type Event = CloudActionConfirmationDialogEvent;
}

impl View for CloudActionConfirmationDialog {
    fn ui_name() -> &'static str {
        "CloudActionConfirmationDialog"
    }

    fn render(&self, app: &AppContext) -> Box<dyn Element> {
        let appearance = Appearance::as_ref(app);

        let default_button_styles = UiComponentStyles {
            font_size: Some(BUTTON_FONT_SIZE),
            font_family_id: Some(appearance.ui_font_family()),
            font_color: Some(
                appearance
                    .theme()
                    .main_text_color(appearance.theme().background())
                    .into(),
            ),
            font_weight: Some(Weight::Bold),
            border_radius: Some(CornerRadius::with_all(Radius::Pixels(BUTTON_BORDER_RADIUS))),
            border_color: Some(appearance.theme().outline().into()),
            border_width: Some(BORDER_WIDTH),
            padding: Some(Coords::uniform(BUTTON_PADDING)),
            background: Some(appearance.theme().surface_1().into()),
            ..Default::default()
        };

        let primary_button_styles = UiComponentStyles {
            background: Some(appearance.theme().accent_button_color().into()),
            border_color: Some(appearance.theme().accent_button_color().into()),
            ..default_button_styles
        };

        let primary_hovered_and_clicked_styles = UiComponentStyles {
            background: Some(blended_colors::accent_hover(appearance.theme()).into()),
            border_color: Some(blended_colors::accent_hover(appearance.theme()).into()),
            ..primary_button_styles
        };

        let cancel_button = appearance
            .ui_builder()
            .button(ButtonVariant::Secondary, self.cancel_mouse_state.clone())
            .with_style(UiComponentStyles {
                font_size: Some(BUTTON_FONT_SIZE),
                font_weight: Some(Weight::Bold),
                padding: Some(Coords::uniform(BUTTON_PADDING)),
                ..Default::default()
            })
            .with_text_label(CANCEL_TEXT.into())
            .build()
            .with_cursor(Cursor::PointingHand)
            .on_click(move |ctx, _, _| {
                ctx.dispatch_typed_action(CloudActionConfirmationDialogAction::Cancel)
            })
            .finish();

        let confirm_hoverable = appearance
            .ui_builder()
            .button_with_custom_styles(
                ButtonVariant::Basic,
                self.confirm_mouse_state.clone(),
                primary_button_styles,
                Some(primary_hovered_and_clicked_styles),
                Some(primary_hovered_and_clicked_styles),
                Some(primary_hovered_and_clicked_styles),
            )
            .with_text_label(self.confirm_button_text())
            .build()
            .with_cursor(Cursor::PointingHand)
            .on_click(move |ctx, _, _| {
                ctx.dispatch_typed_action(CloudActionConfirmationDialogAction::Confirm)
            });

        let confirm_button = if self.confirmation_button_enabled {
            confirm_hoverable.finish()
        } else {
            confirm_hoverable.disable().finish()
        };

        let dialog = Dialog::new(
            self.title_text(),
            Some(self.body_text()),
            dialog_styles(appearance),
        )
        .with_bottom_row_child(cancel_button)
        .with_bottom_row_child(
            Container::new(confirm_button)
                .with_margin_left(12.)
                .finish(),
        )
        .with_width(DIALOG_WIDTH)
        .build()
        .finish();

        Dismiss::new(dialog)
            .prevent_interaction_with_other_elements()
            .on_dismiss(|ctx, _app| {
                ctx.dispatch_typed_action(CloudActionConfirmationDialogAction::Cancel)
            })
            .finish()
    }
}

impl TypedActionView for CloudActionConfirmationDialog {
    type Action = CloudActionConfirmationDialogAction;

    fn handle_action(&mut self, action: &Self::Action, ctx: &mut ViewContext<Self>) {
        match action {
            CloudActionConfirmationDialogAction::Cancel => {
                ctx.emit(CloudActionConfirmationDialogEvent::Cancel)
            }
            CloudActionConfirmationDialogAction::Confirm => {
                self.set_confirmation_button_enabled(false);
                ctx.notify();
                ctx.emit(CloudActionConfirmationDialogEvent::Confirm)
            }
        }
    }
}
